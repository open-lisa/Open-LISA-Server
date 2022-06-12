from open_lisa.domain.command.command import Command
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.exceptions.invalid_scpi_syntax_for_command_parameters import InvalidSCPISyntaxForCommandParameters

SCPI_PARAMETER_VALUE_PLACEHOLDER = "{}"


class SCPICommand(Command):
    def __init__(self, name, pyvisa_resource, scpi_template_syntax, parameters=CommandParameters()):
        """Creates a new SCPI command

        Args:
            name (string): the string syntax that identifies the command
            pyvisa_resource (pyvisa.Resource): a valid pyvisa Resource instance https://pyvisa.readthedocs.io/en/latest/api/resources.html#pyvisa.resources.Resource
            scpi_template_syntax (string): SCPI command to be sent to pyvisa_resource, '{}' placeholders will be populated with parameters. Example 'CH{}:VOLts {}'
            parameters (CommandParameters): an instance of command parameters
        """
        self._name = name
        self._resource = pyvisa_resource
        self._scpi_template_syntax = scpi_template_syntax

        assert isinstance(parameters, CommandParameters)
        self._parameters = parameters

        if self._parameters.amount != scpi_template_syntax.count(SCPI_PARAMETER_VALUE_PLACEHOLDER):
            raise InvalidSCPISyntaxForCommandParameters(
                syntax=scpi_template_syntax, placeholders_amount=self._parameters.amount)

    def execute(self, params_values=[]):
        self._parameters.validate_parameters_values(params_values)

        scpi_command = self.__generate_scpi_command_with_injected_params(
            params_values)

        # TODO: test that with write + read_raw is enough https://trello.com/c/tLuwyeAD/26-refactor-tipos-de-comandos-scpi
        self._resource.write(scpi_command)
        return self._resource.read_raw()

    def __generate_scpi_command_with_injected_params(self, params_values):
        if len(params_values):
            return self._scpi_template_syntax.format(*params_values)
        else:
            return self._scpi_template_syntax