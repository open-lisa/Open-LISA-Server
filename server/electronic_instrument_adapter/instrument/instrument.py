import json
import logging
import sys
import ctypes

import pyvisa
from .constants import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE, INSTRUMENT_STATUS_NOT_REGISTERED, COMMAND_TYPE_SET, COMMAND_TYPE_QUERY, COMMAND_TYPE_QUERY_BUFFER, COMMAND_TYPE_C_LIB, TYPE_FLOAT, TYPE_INT
from electronic_instrument_adapter.exceptions.command_not_found_error import CommandNotFoundError
from electronic_instrument_adapter.exceptions.invalid_parameter_error import InvalidParameterError
from electronic_instrument_adapter.exceptions.invalid_amount_parameters_error import InvalidAmountParametersError
from electronic_instrument_adapter.exceptions.instrument_unavailable_error import InstrumentUnavailableError

class Instrument:
    def __init__(self, id, brand, model, description, command_file):
        self.id = id
        self.brand = brand
        self.model = model
        self.description = description
        self.command_file = None
        self.device = None
        self.commands_map = None

        if command_file:
            self.command_file = command_file
            self.load_commands()

        self.update_status()

    def load_commands(self):
        try:
            with open('electronic_instrument_adapter/instrument/specs/{}'.format(self.command_file)) as file:
                self.commands_map = json.load(file)
        except OSError as e:
            logging.error("[Instrument][load_commands][OPEN_FILE_FAIL] - {}".format(e))

    def update_status(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        self.device = None

        # Debugging purposes
        if "MOCK_INSTRUMENT" in self.brand:
            self.status = INSTRUMENT_STATUS_AVAILABLE
            return

        if resources.__contains__(self.id):
            self.device = rm.open_resource(self.id)
            self.status = INSTRUMENT_STATUS_AVAILABLE
        elif self.commands_map:
            self.status = INSTRUMENT_STATUS_UNAVAILABLE
        else:
            self.status = INSTRUMENT_STATUS_NOT_REGISTERED

    def __str__(self):
        return "{}\n\t" \
               "Brand    : {}\n\t" \
               "Model    : {}\n\t" \
               "ID       : {}\n\t" \
               "Cmd File : {}\n\t" \
               "Status   : {}".format(
            self.description,
            self.brand,
            self.model,
            self.id,
            self.command_file,
            self.status)

    def as_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "status": self.status,
            "description": self.description
        }

    def send_command(self, command):
        if not self.status == INSTRUMENT_STATUS_AVAILABLE:
            raise InstrumentUnavailableError("instrument {} {} not available for sending command".format(self.brand, self.model))

        self.validate_command(command)
        commands_parts = command.split(' ')
        command_base = commands_parts[0]

        command_type = self.commands_map[command_base]['type']

        # Inject command parameters
        command_with_params = self.__generate_command_with_injected_params(command)

        if command_type == COMMAND_TYPE_SET:
            written_bytes = self.device.write(command_with_params)
            return str(written_bytes)
        elif command_type == COMMAND_TYPE_QUERY:
            response = self.device.query(command_with_params)
            return response
        elif command_type == COMMAND_TYPE_QUERY_BUFFER:
            self.device.write(command_with_params)
            response = self.device.read_raw()
            return response
        elif command_type == COMMAND_TYPE_C_LIB:
            # For now, only return strings
            return str(self.__process_c_lib_call(command))

    def validate_command(self, command):
        commands_parts = command.split(' ')
        command_base = commands_parts[0]
        if command_base not in self.commands_map:
            raise CommandNotFoundError

        number_of_parameters_sent = len(commands_parts) - 1
        if 'params' in self.commands_map[command_base]:
            number_of_parameters_required = len(self.commands_map[command_base]['params'])
            if number_of_parameters_required != number_of_parameters_sent:
                raise InvalidAmountParametersError(number_of_parameters_sent, number_of_parameters_required)

            for required_param_info in self.commands_map[command_base]['params']:
                sent_param = commands_parts[required_param_info['position']]
                if not self._valid_format(sent_param, required_param_info):
                    raise InvalidParameterError(required_param_info['position'],
                                                required_param_info['type'],
                                                required_param_info['example'])

    def _valid_format(self, sent_param, required_param_info):
        if required_param_info['type'] == "float":
            try:
                float(sent_param)
            except ValueError:
                return False

            return True

        if required_param_info['type'] == "int":
            try:
                int(sent_param)
            except ValueError:
                return False

            return True

        else:
            return False

    def __generate_command_with_injected_params(self, command):
        commands_parts = command.split(' ')
        command_name = commands_parts[0]
        if 'params' in self.commands_map[command_name] and len(commands_parts) > 1:
            return self.commands_map[command_name]['command'].format(*commands_parts[1:])

    def __map_type_to_ctype(self, type):
        if type == TYPE_INT:
            return ctypes.c_int
        elif type == TYPE_FLOAT:
            return ctypes.c_float
        else:
            # todo: raise exception?
            pass

    def __convert_param_value(self, type, value):
        if type == TYPE_FLOAT:
            return float(value)
        if type == TYPE_INT:
            return int(value)
        return value

    def __process_c_lib_call(self, command):
        commands_parts = command.split(' ')
        command_name = commands_parts[0]
        command_obj = self.commands_map[command_name]
        lib_path = command_obj["lib_path"]
        c_function_name = command_obj["command"]
        # Load the shared library into c types.
        c_lib = ctypes.CDLL(lib_path)

        # Set returning type for marshalling
        return_type = command_obj["return"]["type"]
        c_lib[c_function_name].restype = self.__map_type_to_ctype(return_type)

        # Generate function arguments
        arguments = [self.__map_type_to_ctype(param_obj["type"])(self.__convert_param_value(param_obj["type"], param_value)) for param_obj, param_value  in zip(command_obj["params"], commands_parts[1:])]

        # Call function and return result
        return c_lib[c_function_name](*arguments)

