import ctypes
from enum import Enum
from open_lisa.exceptions.invalid_command_parameter_value_error import InvalidCommandParameterValueError


class CommandReturnType(Enum):
    VOID = "void"
    FLOAT = "float"
    INT = "int"
    STRING = "string"
    BYTES = "bytes"

    def __str__(self):
        return self.name


class CommandReturn():
    def __init__(self, type=CommandReturnType.VOID, description=''):
        assert isinstance(type, CommandReturnType)
        self.type = type
        self.description = description

    @staticmethod
    def from_dict(parameter_dict):
        return CommandReturn(
            type=CommandReturnType[parameter_dict["type"]],
            description=parameter_dict["description"],
        )

    def to_dict(self):
        return {
            "type": str(self.type),
            "description": self.description
        }

    def to_ctype(self):
        if self.type == CommandReturnType.INT:
            return ctypes.c_int
        elif self.type == CommandReturnType.FLOAT:
            return ctypes.c_float
        elif self.type == CommandReturnType.BYTES:
            # NOTE: functions that returns bytes should return int error codes.
            # If code is 0 the bytes were successfully saved into the file buffer
            return ctypes.c_int
        elif self.type == CommandReturnType.STRING:
            return ctypes.c_char_p
        elif self.type == CommandReturnType.VOID:
            return None
