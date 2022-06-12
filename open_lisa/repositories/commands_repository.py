from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.command_parameter import CommandParameter, CommandParameterType
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

    def get_instrument_commands(self, instrument_id, pyvisa_resource=None):
        command_dicts = self.get_by_key_value("instrument_id", instrument_id)
        return [
            self.__create_command_object_from_dict(cd, pyvisa_resource) for cd in command_dicts
        ]

    def __generate_params_list(self, parameters: CommandParameters):
        return [
            self.__command_parameter_to_dict(p) for p in parameters._parameters
        ]

    def __command_parameter_to_dict(self, param: CommandParameter):
        return {
            "position": param.position,
            "type": str(param.type),
            "description": param.description
        }

    def __create_command_object_from_dict(self, command_dict, pyvisa_resource):
        if command_dict["type"] == str(CommandType.SCPI):
            return SCPICommand(
                name=command_dict["name"],
                pyvisa_resource=pyvisa_resource,
                scpi_template_syntax=command_dict["command"],
                parameters=self.__create_command_parameters_object_from_dict(
                    command_dict["params"]),
                description=command_dict["description"]
            )
        # TODO is type CLibCommand

    def __create_command_parameters_object_from_dict(self, parameters_dict):
        command_parameters = CommandParameters()
        for pd in parameters_dict:
            command_parameters.add(
                self.__create_command_parameter_object_from_dict(pd))
        return command_parameters

    def __create_command_parameter_object_from_dict(self, parameter_dict):
        return CommandParameter(
            type=CommandParameterType[parameter_dict["type"]],
            position=parameter_dict["position"],
            description=parameter_dict["description"],
        )
