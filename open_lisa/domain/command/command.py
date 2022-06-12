from enum import Enum

from open_lisa.domain.command.command_parameters import CommandParameters


class CommandType(Enum):
    SCPI = "scpi"
    CLIB = "clib"

    def __str__(self):
        return self.name


class Command:
    def __init__(self, name, command, parameters, type, description) -> None:
        self.name = name
        self.command = command
        self.type = type
        self.description = description

        assert isinstance(parameters, CommandParameters)
        self.parameters = parameters

    def execute(self, params):
        raise NotImplementedError("Please Implement this method: execute")
