import json

import pyvisa
from .constants import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE
from electronic_instrument_adapter.exceptions.command_not_found_error import CommandNotFoundError
from electronic_instrument_adapter.exceptions.invalid_parameter_error import InvalidParameterError
from electronic_instrument_adapter.exceptions.invalid_amount_parameters_error import InvalidAmountParametersError
from electronic_instrument_adapter.exceptions.instrument_unavailable_error import InstrumentUnavailableError

class Instrument:
    def __init__(self, id, brand, model, description):
        self.id = id
        self.brand = brand
        self.model = model
        self.description = description
        self.device = None
        self.status = INSTRUMENT_STATUS_UNAVAILABLE
        self.commands_map = None
        self.load_commands()

        self.set_status()

    def load_commands(self):
        with open('electronic_instrument_adapter/instrument/specs/{}_{}_cmd.json'.format(
                self.brand, self.model)) as file:
            self.commands_map = json.load(file)

    def set_status(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        if resources.__contains__(self.id):
            self.device = rm.open_resource(self.id)
            self.status = INSTRUMENT_STATUS_AVAILABLE
        else:
            self.device = None
            self.status = INSTRUMENT_STATUS_UNAVAILABLE

    def __str__(self):
        return "{}\n\t" \
               "Brand  : {}\n\t" \
               "Model  : {}\n\t" \
               "ID     : {}\n\t" \
               "Status : {}".format(
            self.description,
            self.brand,
            self.model,
            self.id,
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
        if command_type == "set":
            written_bytes = self.device.write(self.commands_map[command_base]['command'])
            # todo: handlear el caso en que written_bytes = 0 por posible error en conexión
        elif command_type == "query":
            response = self.device.query(self.commands_map[command_base]['command'])
            return str(response)
        elif command_type == "query_buffer":
            self.device.query(self.commands_map[command_base]['command'])
            response = self.device.read_raw()
            return str(response)
        else:
            # todo: handlear este caso en un validador de formato general para el _cmd.json
            pass

        return ""

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

        else:
            return False
