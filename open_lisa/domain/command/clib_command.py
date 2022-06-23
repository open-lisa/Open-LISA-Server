import ctypes
import logging
import os
from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn, CommandReturnType
from open_lisa.exceptions.command_execution_error import CommandExecutionError
from open_lisa.exceptions.invalid_clib_command_function_name import InvalidCLibCommandFunctionNameError
from open_lisa.exceptions.invalid_clib_command_lib_file import InvalidCLibCommandLibFileError

C_LIBS_PATH = 'data/clibs/'

TMP_BUFFER_FILE = "tmp_file_buffer.bin"


class CLibCommand(Command):
    def __init__(self, name, lib_function, lib_file_name, parameters=CommandParameters(), command_return=CommandReturn(), description=''):
        """Creates a new SCPI command

        Args:
            name (string): the string syntax that identifies the command
            lib_function (string): Lib function to be called in the lib file
            lib_file_name (string): Lib file name (C libs should be stored in C_LIBS_PATH)
            parameters (CommandParameters): an instance of command parameters
        """
        super().__init__(name=name, command=lib_function,
                         parameters=parameters, type=CommandType.CLIB, description=description)

        self.lib_function = lib_function
        self.lib_file_name = lib_file_name
        self.command_return = command_return

        try:
            # Load the shared library into c types.
            self._c_lib = ctypes.CDLL(self.lib_file_name)
        except Exception as e:
            logging.error('[CLibCommand][__init__][CDLL] error: {}'.format(e))
            raise InvalidCLibCommandLibFileError(lib_name=self.lib_file_name)

        try:
            # c_lib is an object instance and function name is accessed like
            # an object property, doing c_lib[self.lib_function] is incorrect
            self._c_function = getattr(self._c_lib, self.lib_function)
        except Exception as e:
            logging.error(
                '[CLibCommand][__init__][INVALID_LIB_FUNCTION] error: {}'.format(e))
            raise InvalidCLibCommandFunctionNameError(
                function_name=self.lib_function, lib_name=self.lib_file_name)

        # Set returning type for marshalling
        command_return_ctype = self.command_return.to_ctype()
        self._c_function.restype = command_return_ctype

    @staticmethod
    def from_dict(command_dict, pyvisa_resource):
        return CLibCommand(
            name=command_dict["name"],
            lib_function=pyvisa_resource,
            lib_file_name=command_dict["lib_file_name"],
            parameters=CommandParameters.from_dict(command_dict["params"]),
            description=command_dict["description"]
        )

    def to_dict(self, instrument_id):
        return {
            "instrument_id": instrument_id,
            "name": self.name,
            "command": self.lib_function,
            "type": str(self.type),
            "lib_file_name": self.lib_file_name,
            "description": self.description,
            "params": self.parameters.to_dict(),
            "return": self.command_return.to_dict()
        }

    def execute(self, params_values=[]):
        self.parameters.validate_parameters_values(params_values)

        # Generate C function arguments
        arguments = self.parameters.parameters_values_to_c_function_arguments(
            params_values)

        if self.command_return.type == CommandReturnType.BYTES:
            arguments.append(ctypes.c_char_p(TMP_BUFFER_FILE.encode()))
            error_code = self._c_function(*arguments)
            if error_code != 0:
                logging.error("[CLibCommand][command={}] fail calling C function that returns bytes, error code is {}".format(
                    self.name, error_code))
                raise CommandExecutionError(command=self.name, additional_info="C function {} returned error_code {}".format(
                    self.lib_function, error_code))
            else:
                data = bytes()
                with open(TMP_BUFFER_FILE, "rb") as f:
                    data = f.read()

                # Delete file
                os.remove(TMP_BUFFER_FILE)

                return bytes(data)
        else:
            result = self._c_function(*arguments)
            # CommandReturnType.STRING does not exist in C, for that reason char* in C
            # is mapped to bytes() in Python and should be decoded
            return result.decode() if self.command_return.type == CommandReturnType.STRING else result
