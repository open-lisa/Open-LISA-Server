import os
from open_lisa.domain.command.clib_command import CLibCommand
from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.scpi_command import SCPICommand
from open_lisa.repositories.json_repository import JSONRepository


class CommandsRepository(JSONRepository):
    def __init__(self, commands_db_path=os.getenv("DATABASE_COMMANDS_PATH"), clibs_path=os.getenv("CLIBS_PATH")) -> None:
        commands_db_path = os.getenv(
            "DATABASE_COMMANDS_PATH") if not commands_db_path else commands_db_path
        clibs_path = os.getenv(
            "CLIBS_PATH") if not clibs_path else clibs_path
        super().__init__(commands_db_path)
        self._clibs_path = clibs_path

    def add(self, command: Command, instrument_id):
        if isinstance(command, Command):
            return self._db.add(command.to_dict(instrument_id))

    def get_instrument_commands(self, instrument_id, pyvisa_resource=None):
        command_dicts = self.get_by_key_value("instrument_id", instrument_id)
        return [
            self.__deserialize_commands(cd, pyvisa_resource) for cd in command_dicts
        ]

    def __deserialize_commands(self, command_dict, pyvisa_resource):
        if command_dict["type"] == str(CommandType.SCPI):
            return SCPICommand.from_dict(
                command_dict=command_dict,
                pyvisa_resource=pyvisa_resource
            )
        if command_dict["type"] == str(CommandType.CLIB):
            return CLibCommand.from_dict(
                command_dict=command_dict,
                lib_base_path=self._clibs_path,
            )
