import json
import pytest
from open_lisa.domain.instrument.constants import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE
from open_lisa.domain.instrument.instrument import InstrumentType
from open_lisa.exceptions.instrument_not_found import InstrumentNotFoundError
from open_lisa.repositories.instruments_repository import InstrumentRepository
from open_lisa.tests.utils import reset_databases

SOME_VALID_PHYSICAL_ADDRESS = "USB0::0x0699::0x0363::C107676::INSTR"
SOME_INVALID_PHYSICAL_ADDRESS = "USB0::0x0699::0x0363::C107676::UNEXISTING"
SOME_VALID_ID = 1
SOME_INVALID_ID = 999


@pytest.fixture(autouse=True)
def on_each():
    # before each
    reset_databases()
    yield  # run test
    # after each


def test_instruments_repository_should_be_created_with_the_entries_of_json_file():
    repo = InstrumentRepository()
    jsons_string = repo.get_all_as_json()
    jsons = json.loads(jsons_string)

    assert jsons[0]["id"] == 1
    assert jsons[1]["id"] == 2


def test_get_all_should_return_a_list_of_Instrument_instances():
    repo = InstrumentRepository()
    instruments = repo.get_all()

    assert instruments[0].id == 1
    assert instruments[1].id == 2


def test_get_by_physical_address_should_return_an_Instrument_if_there_is_a_match():
    repo = InstrumentRepository()
    i = repo.get_by_physical_address(
        physical_addres=SOME_VALID_PHYSICAL_ADDRESS)
    assert i.physical_address == SOME_VALID_PHYSICAL_ADDRESS


def test_get_by_physical_address_should_raise_exception_if_there_is_no_match():
    with pytest.raises(InstrumentNotFoundError):
        repo = InstrumentRepository()
        repo.get_by_physical_address(
            physical_addres=SOME_INVALID_PHYSICAL_ADDRESS)


def test_get_by_id_should_return_an_Instrument_if_there_is_a_match():
    repo = InstrumentRepository()
    i = repo.get_by_id(
        id=SOME_VALID_ID)
    assert i.id == SOME_VALID_ID


def test_get_by_id_should_raise_exception_if_there_is_no_match():
    with pytest.raises(InstrumentNotFoundError):
        repo = InstrumentRepository()
        repo.get_by_id(
            id=SOME_INVALID_ID)


def test_seed_scpi_instruments_should_be_unavailable_since_they_are_not_detected_by_pyvisa():
    repo = InstrumentRepository()
    instruments = repo.get_all()

    for i in instruments:
        if i.type == InstrumentType.SCPI:
            assert i.status == INSTRUMENT_STATUS_UNAVAILABLE


def test_seed_clib_instruments_should_be_available():
    # NOTE: if pyvisa detects CLIB instruments this test should be removed
    repo = InstrumentRepository()
    instruments = repo.get_all()

    for i in instruments:
        if i.type == InstrumentType.CLIB:
            assert i.status == INSTRUMENT_STATUS_AVAILABLE
