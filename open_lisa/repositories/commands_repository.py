from open_lisa.domain.command.command import Command
from open_lisa.domain.command.command_parameter import CommandParameter
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.scpi_command import SCPICommand
from open_lisa.repositories.json_repository import JSONRepository

DEFAULT_PATH = 'database/commands.db.json'


class CommandsRepository(JSONRepository):
    def __init__(self, path=DEFAULT_PATH) -> None:
        super().__init__(path)

    def add(self, command: Command, instrument_id):
        if isinstance(command, SCPICommand):
            return self._db.add({
                "instrument_id": instrument_id,
                "name": command.name,
                "command": command.command,
                "type": str(command.type),
                "description": command.description,
                "params": self.__generate_params_list(command.parameters)
            })

        # TODO is instance CLibCommand

    def __generate_params_list(self, parameters: CommandParameters):
        return [self.__command_parameter_to_dict(p) for p in parameters._parameters]

    def __command_parameter_to_dict(self, param: CommandParameter):
        return {
            "position": param.position,
            "type": str(param.type),
            "description": param.description
        }
