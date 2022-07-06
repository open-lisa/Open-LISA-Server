import base64
import pytest
from pytest_mock import MockerFixture

from open_lisa.domain.command.command_parameter import CommandParameter, CommandParameterType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn, CommandReturnType
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

COMMAND_RETURN_BYTES = CommandReturn(type=CommandReturnType.BYTES)
COMMAND_RETURN_VOID = CommandReturn(type=CommandReturnType.VOID)
COMMAND_RETURN_INT = CommandReturn(type=CommandReturnType.INT)


class MockPyvisaResource:
    def __init__(self):
        self.read_raw_mock_result = None
        self.write_mock_result = None
        self.query_mock_result = None

    def write(self, command):
        return self.write_mock_result

    def read_raw(self):
        return self.read_raw_mock_result

    def query(self, command):
        return self.query_mock_result


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


def test_SCPICommand_execute_method_should_write_the_correct_scpi_command_in_pyvisa_resource_if_return_is_void(mocker: MockerFixture):
    expected_command = SET_CHANNEL_VOLTS_SCPI_SYNTAX.format(
        *SET_CHANNEL_VOLTS_PARAMETERS_VALUES)
    mock_result = "{}".format(len(expected_command))
    pyvisa_resource = MockPyvisaResource()
    pyvisa_resource.write_mock_result = mock_result
    write_spy = mocker.spy(pyvisa_resource, 'write')
    scpi_command = SCPICommand(name="set_channel_volts",
                               pyvisa_resource=pyvisa_resource,
                               scpi_template_syntax=SET_CHANNEL_VOLTS_SCPI_SYNTAX,
                               parameters=SET_CHANNEL_VOLTS_PARAMETERS)

    execution_result = scpi_command.execute(
        params_values=SET_CHANNEL_VOLTS_PARAMETERS_VALUES)
    write_spy.assert_called_once_with(
        SET_CHANNEL_VOLTS_SCPI_SYNTAX.format(*SET_CHANNEL_VOLTS_PARAMETERS_VALUES))

    assert execution_result.value == None


def test_SCPICommand_execute_method_should_query_the_correct_scpi_command_in_pyvisa_resource_if_return_is_not_void_or_bytes(mocker: MockerFixture):
    mock_result = 42
    pyvisa_resource = MockPyvisaResource()
    pyvisa_resource.query_mock_result = mock_result
    query_spy = mocker.spy(pyvisa_resource, 'query')
    scpi_command = SCPICommand(
        name="set_channel_volts",
        pyvisa_resource=pyvisa_resource,
        scpi_template_syntax=SET_CHANNEL_VOLTS_SCPI_SYNTAX,
        parameters=SET_CHANNEL_VOLTS_PARAMETERS,
        command_return=COMMAND_RETURN_INT
    )

    execution_result = scpi_command.execute(
        params_values=SET_CHANNEL_VOLTS_PARAMETERS_VALUES)
    query_spy.assert_called_once_with(
        SET_CHANNEL_VOLTS_SCPI_SYNTAX.format(*SET_CHANNEL_VOLTS_PARAMETERS_VALUES))

    assert execution_result.value == mock_result


def test_SCPICommand_execute_method_should_write_the_correct_scpi_command_in_pyvisa_resource_and_call_query_buffer_if_return_type_is_bytes(mocker: MockerFixture):
    mock_result = bytes("raw bytes sent from instrument".encode())
    pyvisa_resource = MockPyvisaResource()
    pyvisa_resource.read_raw_mock_result = mock_result
    write_spy = mocker.spy(pyvisa_resource, 'write')
    read_raw_spy = mocker.spy(pyvisa_resource, 'read_raw')
    scpi_command = SCPICommand(
        name="set_channel_volts",
        pyvisa_resource=pyvisa_resource,
        scpi_template_syntax=SET_CHANNEL_VOLTS_SCPI_SYNTAX,
        parameters=SET_CHANNEL_VOLTS_PARAMETERS,
        command_return=COMMAND_RETURN_BYTES,
    )

    execution_result = scpi_command.execute(
        params_values=SET_CHANNEL_VOLTS_PARAMETERS_VALUES)
    write_spy.assert_called_once_with(
        SET_CHANNEL_VOLTS_SCPI_SYNTAX.format(*SET_CHANNEL_VOLTS_PARAMETERS_VALUES))
    read_raw_spy.assert_called_once()

    assert execution_result.value == base64.b64encode(mock_result).decode()
