from enum import Enum

from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn


class CommandType(Enum):
    SCPI = "scpi"
    CLIB = "clib"

    def __str__(self):
        return self.name


class Command:
    def __init__(self, name, command, parameters, command_return, type, description) -> None:
        self.name = name
        self.command = command
        self.type = type
        self.description = description

        assert isinstance(parameters, CommandParameters)
        assert isinstance(command_return, CommandReturn)
        self.parameters = parameters
        self.command_return = command_return

    @staticmethod
    def from_dict():
        raise NotImplementedError("Please Implement this method: from_dict")

    def to_dict(self):
        raise NotImplementedError("Please Implement this method: to_dict")

    def execute(self, params):
        raise NotImplementedError("Please Implement this method: execute")
