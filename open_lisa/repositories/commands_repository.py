import os

from open_lisa.domain.command.clib_command import CLibCommand
from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.scpi_command import SCPICommand
from open_lisa.exceptions.command_creation_error import CommandCreationError
from open_lisa.exceptions.command_deletion_error import CommandDeletionError
from open_lisa.repositories.json_repository import JSONRepository


class CommandsRepository(JSONRepository):
    def __init__(self, commands_db_path=os.getenv("DATABASE_COMMANDS_PATH"), clibs_path=os.getenv("CLIBS_PATH")) -> None:
        commands_db_path = os.getenv(
            "DATABASE_COMMANDS_PATH") if not commands_db_path else commands_db_path
        clibs_path = os.getenv(
            "CLIBS_PATH") if not clibs_path else clibs_path
        super().__init__(commands_db_path)
        self._clibs_path = clibs_path

    def add(self, command, instrument_id=None):
        if isinstance(command, Command):
            return self._db.add(command.to_dict(int(instrument_id)))
        else:
            return self._db.add(command)

    def create_command(self, new_command, instrument_id, pyvisa_resource=None) -> Command:
        try:
            new_id = self.add(new_command, int(instrument_id))
        except Exception as e:
            raise CommandCreationError(
                "could not create command {}, reason {}".format(new_command, e))
        try:
            recent_created = self.get_by_id(
                new_id, pyvisa_resource=pyvisa_resource)
        except Exception as e:
            self.remove_by_id(id=new_id)
            raise CommandCreationError(
                "command created but there was an error on initialization {}".format(e))
        return recent_created

    def get_by_id(self, id, pyvisa_resource=None, lib_base_path=None) -> Command:
        id = int(id)
        command_json = super().get_by_id(id)

        return self.__deserialize_command(command_json, pyvisa_resource)

    def get_instrument_commands(self, instrument_id, pyvisa_resource=None):
        command_dicts = self.get_by_key_value("instrument_id", instrument_id)
        return [
            self.__deserialize_command(cd, pyvisa_resource) for cd in command_dicts
        ]

    def delete_command(self, command_id):
        command_id = int(command_id)
        try:
            self.remove_by_id(command_id)
        except Exception as e:
            raise CommandDeletionError(
                "could not delete command: {}".format(str(e)))

    def __deserialize_command(self, command_dict, pyvisa_resource):
        if str(command_dict["type"]).lower() == str(CommandType.SCPI).lower():
            return SCPICommand.from_dict(
                command_dict=command_dict,
                pyvisa_resource=pyvisa_resource
            )
        if str(command_dict["type"]).lower() == str(CommandType.CLIB).lower():
            return CLibCommand.from_dict(
                command_dict=command_dict,
                lib_base_path=self._clibs_path,
            )
