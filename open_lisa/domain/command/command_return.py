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
        self.value = None

    @staticmethod
    def from_dict(parameter_dict):
        return CommandReturn(
            type=CommandReturnType[parameter_dict["type"]],
            description=parameter_dict["description"],
        )

    def set_value(self, value):
        # TODO: validate type
        self.value = value

    def to_dict(self):
        return {
            "type": str(self.type),
            "description": self.description
        }
