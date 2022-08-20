import pytest
from pytest_mock import MockerFixture
from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn
from open_lisa.domain.instrument.constants import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE

from open_lisa.domain.instrument.instrument import InstrumentType, Instrument
from open_lisa.exceptions.command_not_found_error import CommandNotFoundError
from open_lisa.exceptions.instrument_unavailable_error import InstrumentUnavailableError

MOCK_COMMAND_EXECUTION_RESULT = "some result"
COMMAND_NAME = "some_command"


class CommandMock(Command):
    def __init__(self, name) -> None:
        super().__init__(
            id=0,
            name=name,
            command="some scpi template",
            parameters=CommandParameters(),
            command_return=CommandReturn(),
            type=CommandType.SCPI,
            description=""
        )

    def execute(slef, params):
        return MOCK_COMMAND_EXECUTION_RESULT


def test_instrument_creation_should_return_an_instance_of_Instrument():
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
        description="some desc"
    )
    assert isinstance(i, Instrument)


def test_instrument_should_be_available_if_pyvisa_resource_is_provided():
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
        pyvisa_resource="some valid pyvisa resource"
    )

    assert i.status == INSTRUMENT_STATUS_AVAILABLE


def test_instrument_should_be_unavailable_if_pyvisa_resource_is_not_provided():
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
        pyvisa_resource=None
    )

    assert i.status == INSTRUMENT_STATUS_UNAVAILABLE


def test_send_command_to_a_not_available_instrument_should_raise_error():
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
    )
    with pytest.raises(InstrumentUnavailableError):
        i.send_command("some_command")


def test_send_command_should_raise_exception_if_command_does_not_exist_for_instrument():
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
        pyvisa_resource="some valid pyvisa resource"
    )
    with pytest.raises(CommandNotFoundError):
        i.send_command("some_unexisting_command")


def test_send_command_should_execute_command(mocker: MockerFixture):
    command = CommandMock(name=COMMAND_NAME)
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
        pyvisa_resource="some valid pyvisa resource",
        commands=[command]
    )
    execute_spy = mocker.spy(command, "execute")
    i.send_command(COMMAND_NAME)
    execute_spy.assert_called_once()


def test_send_command_should_return_command_result():
    command = CommandMock(name=COMMAND_NAME)
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
        pyvisa_resource="some valid pyvisa resource",
        commands=[command]
    )
    result = i.send_command(COMMAND_NAME)
    assert result == MOCK_COMMAND_EXECUTION_RESULT
