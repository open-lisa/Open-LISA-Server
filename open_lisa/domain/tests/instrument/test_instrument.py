import pytest
import pyvisa
from pytest_mock import MockerFixture
from open_lisa.domain.command.command import Command, CommandType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn
from open_lisa.domain.instrument.constants import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE

from open_lisa.domain.instrument.instrument import InstrumentType, Instrument
from open_lisa.exceptions.command_not_found_error import CommandNotFoundError
from open_lisa.exceptions.instrument_unavailable_error import InstrumentUnavailableError
from open_lisa.exceptions.invalid_instrument_type_for_managing_visa_attributes_error import InvalidInstrumentTypeForManagingVisaAttributes


MOCK_COMMAND_EXECUTION_RESULT = "some result"
COMMAND_NAME = "some_command"


class MockPyvisaResource:
    def __init__(self):
        self.set_attribute_mock_result = None
        self.get_attribute_mock_result = None

    def set_visa_attribute(self, attribute, state):
        return self.set_attribute_mock_result

    def get_visa_attribute(self, attribute):
        return self.get_attribute_mock_result


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


def test_set_visa_attribute_raises_if_instrument_is_not_available():
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
    )
    with pytest.raises(InstrumentUnavailableError):
        i.set_visa_attribute(
            pyvisa.constants.ResourceAttribute.interface_type, 0xFFFFFF)


def test_set_visa_attribute_raises_if_instrument_is_not_SCPI_type():
    i = Instrument(
        id=1,
        physical_address=None,
        brand="some brand",
        model="some model",
        type=InstrumentType.CLIB,
    )
    with pytest.raises(InvalidInstrumentTypeForManagingVisaAttributes):
        i.set_visa_attribute(
            pyvisa.constants.ResourceAttribute.interface_type, 0xFFFFFF)


def test_set_visa_attribute_should_call_pyvisa_resource_set_visa_attribute(mocker: MockerFixture):
    pyvisa_resource_mock = MockPyvisaResource()
    some_visa_attribute = pyvisa.constants.ResourceAttribute.interface_type
    some_visa_attribute_state = 0xfeafea
    some_visa_status_code = pyvisa.constants.StatusCode.error_abort
    pyvisa_resource_mock.set_attribute_mock_result = some_visa_status_code
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
        pyvisa_resource=pyvisa_resource_mock
    )
    set_attribute_spy = mocker.spy(pyvisa_resource_mock, "set_visa_attribute")
    result = i.set_visa_attribute(
        some_visa_attribute, some_visa_attribute_state)
    set_attribute_spy.assert_called_once()
    set_attribute_spy.assert_called_once_with(
        some_visa_attribute, some_visa_attribute_state)
    assert result == "{}".format(some_visa_status_code.value)


def test_get_visa_attribute_raises_if_instrument_is_not_available():
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
    )
    with pytest.raises(InstrumentUnavailableError):
        i.get_visa_attribute(
            pyvisa.constants.ResourceAttribute.interface_type)


def test_get_visa_attribute_raises_if_instrument_is_not_SCPI_type():
    i = Instrument(
        id=1,
        physical_address=None,
        brand="some brand",
        model="some model",
        type=InstrumentType.CLIB,
    )
    with pytest.raises(InvalidInstrumentTypeForManagingVisaAttributes):
        i.get_visa_attribute(
            pyvisa.constants.ResourceAttribute.interface_type)


def test_get_visa_attribute_should_call_pyvisa_resource_get_visa_attribute(mocker: MockerFixture):
    pyvisa_resource_mock = MockPyvisaResource()
    some_visa_attribute = pyvisa.constants.ResourceAttribute.interface_type
    some_visa_attribute_state = 0xfeafea
    pyvisa_resource_mock.get_attribute_mock_result = some_visa_attribute_state
    i = Instrument(
        id=1,
        physical_address="USB:1234",
        brand="some brand",
        model="some model",
        type=InstrumentType.SCPI,
        pyvisa_resource=pyvisa_resource_mock
    )
    get_attribute_spy = mocker.spy(pyvisa_resource_mock, "get_visa_attribute")
    result = i.get_visa_attribute(some_visa_attribute)
    get_attribute_spy.assert_called_once()
    get_attribute_spy.assert_called_once_with(
        some_visa_attribute)
    assert result == str(some_visa_attribute_state)
