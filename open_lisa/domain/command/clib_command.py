import ctypes
import logging
import os
from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn, CommandReturnType

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

        # Load the shared library into c types.
        c_lib = ctypes.CDLL(self.lib_file_name)

        # c_lib is an object instance and function name is accessed like
        # an object property, doing c_lib[self.lib_function] is incorrect
        c_function = getattr(c_lib, self.lib_function)

        # Set returning type for marshalling
        command_return_ctype = self.command_return.to_ctype()
        c_function.restype = command_return_ctype

        # Generate C function arguments
        arguments = self.parameters.parameters_values_to_c_function_arguments(
            params_values)

        if self.command_return.type == CommandReturnType.BYTES:
            arguments.append(ctypes.c_char_p(TMP_BUFFER_FILE.encode()))
            result = c_function(*arguments)
            if result:
                logging.error("[CLibCommand][command={}] fail calling C function that returns bytes, result code is {}".format(
                    self.name, result))
                return bytes("C function error code {}".format(result).encode())
            else:
                data = bytes()
                with open(TMP_BUFFER_FILE, "rb") as f:
                    data = f.read()

                # Delete file
                os.remove(TMP_BUFFER_FILE)

                return bytes(data)
        else:
            result = c_function(*arguments)
            # ctypes c_char_p is returned as bytes
            return result.decode() if c_function.restype == ctypes.c_char_p else result
