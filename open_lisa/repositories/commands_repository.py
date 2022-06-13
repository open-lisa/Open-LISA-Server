from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.scpi_command import SCPICommand
from open_lisa.repositories.json_repository import JSONRepository

DEFAULT_PATH = 'database/commands.db.json'


class CommandsRepository(JSONRepository):
    def __init__(self, path=DEFAULT_PATH) -> None:
        super().__init__(path)

    def add(self, command: Command, instrument_id):
        if isinstance(command, SCPICommand):
            return self._db.add(command.to_dict(instrument_id))

        # TODO is instance CLibCommand

    def get_instrument_commands(self, instrument_id, pyvisa_resource=None):
        command_dicts = self.get_by_key_value("instrument_id", instrument_id)
        return [
            self.__deserialize_commands(cd, pyvisa_resource) for cd in command_dicts
        ]

    def __deserialize_commands(self, command_dict, pyvisa_resource):
        if command_dict["type"] == str(CommandType.SCPI):
            return SCPICommand.from_dict(command_dict=command_dict, pyvisa_resource=pyvisa_resource)
        # TODO is type CLibCommand
