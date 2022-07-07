from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.command_execution_result import CommandExecutionResult
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn, CommandReturnType
from open_lisa.exceptions.invalid_scpi_syntax_for_command_parameters import InvalidSCPISyntaxForCommandParameters
from open_lisa.utils.date import get_UTC_timestamp

SCPI_PARAMETER_VALUE_PLACEHOLDER = "{}"


class SCPICommand(Command):
    def __init__(self, name, pyvisa_resource, scpi_template_syntax, parameters=CommandParameters(), command_return=CommandReturn(), description=''):
        """Creates a new SCPI command

        Args:
            name (string): the string syntax that identifies the command
            pyvisa_resource (pyvisa.Resource): a valid pyvisa Resource instance https://pyvisa.readthedocs.io/en/latest/api/resources.html#pyvisa.resources.Resource
            scpi_template_syntax (string): SCPI command to be sent to pyvisa_resource, '{}' placeholders will be populated with parameters. Example 'CH{}:VOLts {}'
            parameters (CommandParameters): an instance of command parameters
            command_return (CommandReturn): an instance of command return
        """
        super().__init__(name=name, command=scpi_template_syntax,
                         parameters=parameters, command_return=command_return, type=CommandType.SCPI, description=description)
        self._resource = pyvisa_resource
        self._scpi_template_syntax = scpi_template_syntax

        if self.parameters.amount != scpi_template_syntax.count(SCPI_PARAMETER_VALUE_PLACEHOLDER):
            raise InvalidSCPISyntaxForCommandParameters(
                syntax=scpi_template_syntax, placeholders_amount=self.parameters.amount)

    @staticmethod
    def from_dict(command_dict, pyvisa_resource):
        return SCPICommand(
            name=command_dict["name"],
            pyvisa_resource=pyvisa_resource,
            scpi_template_syntax=command_dict["command"],
            parameters=CommandParameters.from_dict(command_dict["params"]),
            command_return=CommandReturn.from_dict(command_dict["return"]),
            description=command_dict["description"]
        )

    def to_dict(self, instrument_id):
        return {
            "instrument_id": instrument_id,
            "name": self.name,
            "command": self.command,
            "type": str(self.type),
            "description": self.description,
            "params": self.parameters.to_dict(),
            "return": self.command_return.to_dict(),
        }

    def execute(self, params_values=[]):
        self.parameters.validate_parameters_values(params_values)

        scpi_command = self.__generate_scpi_command_with_injected_params(
            params_values)

        command_execution_start = get_UTC_timestamp()
        if self.command_return.type == CommandReturnType.BYTES:
            # returns read_raw as in QUERY_BUFFER
            self._resource.write(scpi_command)
            raw_result_value = self._resource.read_raw()
        elif self.command_return.type == CommandReturnType.VOID:
            # returns written bytes as in type SET
            self._resource.write(scpi_command)
            raw_result_value = None
        else:
            # assumes that is expected to behave as QUERY
            raw_result_value = self._resource.query(scpi_command)

        return CommandExecutionResult(timestamp_execution_start=command_execution_start, type=self.command_return.type, raw_value=raw_result_value)

    def __generate_scpi_command_with_injected_params(self, params_values):
        if len(params_values):
            return self._scpi_template_syntax.format(*params_values)
        else:
            return self._scpi_template_syntax
