import ctypes
import logging
import os
from pathlib import Path

from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.command_execution_result import CommandExecutionResult
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn, CommandReturnType
from open_lisa.exceptions.command_execution_error import CommandExecutionError
from open_lisa.exceptions.invalid_clib_command_function_name import InvalidCLibCommandFunctionNameError
from open_lisa.exceptions.invalid_clib_command_lib_file import InvalidCLibCommandLibFileError
from open_lisa.utils.date import get_UTC_timestamp

TMP_BUFFER_FILE = "tmp_file_buffer.bin"


class CLibCommand(Command):
    def __init__(self, name, lib_function, lib_file_name, id=0, parameters=CommandParameters(), command_return=CommandReturn(), description=''):
        """Creates a new SCPI command

        Args:
            name (string): the string syntax that identifies the command
            lib_function (string): Lib function to be called in the lib file
            lib_file_name (string): Lib file name should be an absolute path in order to find the library
            parameters (CommandParameters): an instance of command parameters
        """
        super().__init__(id=id, name=name, command=lib_function,
                         parameters=parameters, command_return=command_return, type=CommandType.CLIB, description=description)

        self.lib_function = lib_function
        self.lib_file_name = lib_file_name

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
    def from_dict(command_dict, lib_base_path):
        subfolder_path = command_dict["metadata"]["lib_file_name"].replace(
            "/", os.sep)
        return CLibCommand(
            id=command_dict["id"],
            name=command_dict["name"],
            lib_function=command_dict["command"],
            lib_file_name=os.path.join(
                lib_base_path, subfolder_path),
            parameters=CommandParameters.from_dict(command_dict["params"]),
            command_return=CommandReturn.from_dict(command_dict["return"]),
            description=command_dict["description"]
        )

    def to_dict(self, instrument_id):
        lib_file_path_parts = list(Path(self.lib_file_name).parts)
        lib_file_relative_path = lib_file_path_parts[lib_file_path_parts.index(
            'clibs')+1:]
        return {
            "id": str(self.id),
            "instrument_id": int(instrument_id),
            "name": self.name,
            "command": self.lib_function,
            "type": str(self.type),
            "description": self.description,
            "params": self.parameters.to_dict(),
            "return": self.command_return.to_dict(),
            "metadata": {
                # only return filename
                "lib_file_name": Path(*lib_file_relative_path).__str__()
            }
        }

    def execute(self, params_values=[]):
        self.parameters.validate_parameters_values(params_values)

        # Generate C function arguments
        arguments = self.parameters.parameters_values_to_c_function_arguments(
            params_values)

        if self.command_return.type == CommandReturnType.BYTES:
            # NOTE: functions that returns bytes should return int error codes.
            # If code is 0 the bytes were successfully saved into the file buffer
            arguments.append(ctypes.c_char_p(TMP_BUFFER_FILE.encode()))
            command_execution_start = get_UTC_timestamp()
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

                raw_result_value = bytes(data)
                return CommandExecutionResult(timestamp_execution_start=command_execution_start, type=self.command_return.type, raw_value=raw_result_value)
        else:
            command_execution_start = get_UTC_timestamp()
            result = self._c_function(*arguments)
            # CommandReturnType.STRING does not exist in C, for that reason char* in C
            # is mapped to bytes() in Python and should be decoded
            raw_result_value = result.decode() \
                if self.command_return.type == CommandReturnType.STRING else result
            return CommandExecutionResult(timestamp_execution_start=command_execution_start, type=self.command_return.type, raw_value=raw_result_value)
