import pytest
from pytest_mock import MockerFixture

from open_lisa.domain.command.command_parameter import CommandParameter, CommandParameterType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.scpi_command import SCPICommand
from open_lisa.exceptions.invalid_scpi_syntax_for_command_parameters import InvalidSCPISyntaxForCommandParameters


SET_CHANNEL_VOLTS_NAME = "set_channel_volts"
SET_CHANNEL_VOLTS_SCPI_SYNTAX = "CH{} VOLts {}"

SET_CHANNEL_VOLTS_PARAMETERS = CommandParameters()
SET_CHANNEL_VOLTS_PARAMETERS.add(CommandParameter(
    type=CommandParameterType.INT, position=1))
SET_CHANNEL_VOLTS_PARAMETERS.add(CommandParameter(
    type=CommandParameterType.FLOAT, position=2))
SET_CHANNEL_VOLTS_PARAMETERS_VALUES = [1, 5.0]


class MockPyvisaResource:
    def __init__(self):
        self.read_raw_mock_result = None

    def write(self, str):
        pass

    def read_raw(self):
        return self.read_raw_mock_result


def test_SCPICommand_creation():
    scpi_command = SCPICommand(name="set_channel_volts",
                               pyvisa_resource=None,
                               scpi_template_syntax=SET_CHANNEL_VOLTS_SCPI_SYNTAX,
                               parameters=SET_CHANNEL_VOLTS_PARAMETERS)
    assert isinstance(scpi_command, SCPICommand)


def test_SCPICommand_invalid_creation():
    with pytest.raises(InvalidSCPISyntaxForCommandParameters):
        SCPICommand(name="set_channel_volts",
                    pyvisa_resource=None,
                    scpi_template_syntax="CH {} {} {}",
                    parameters=SET_CHANNEL_VOLTS_PARAMETERS)


def test_SCPICommand_execute_method_should_write_the_correct_scpi_command_in_pyvisa_resource(mocker: MockerFixture):
    mock_result = bytes("result bytes...".encode())
    pyvisa_resource = MockPyvisaResource()
    pyvisa_resource.read_raw_mock_result = mock_result
    write_spy = mocker.spy(pyvisa_resource, 'write')
    scpi_command = SCPICommand(name="set_channel_volts",
                               pyvisa_resource=pyvisa_resource,
                               scpi_template_syntax=SET_CHANNEL_VOLTS_SCPI_SYNTAX,
                               parameters=SET_CHANNEL_VOLTS_PARAMETERS)

    execution_result = scpi_command.execute(
        params_values=SET_CHANNEL_VOLTS_PARAMETERS_VALUES)
    write_spy.assert_called_once_with(
        SET_CHANNEL_VOLTS_SCPI_SYNTAX.format(*SET_CHANNEL_VOLTS_PARAMETERS_VALUES))

    assert execution_result == mock_result
