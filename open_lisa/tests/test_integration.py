import pytest
import os
import Open_LISA_SDK
from open_lisa.api.api import OpenLISA
from open_lisa.config.config import load_config
from open_lisa.protocol.rs232configuration import RS232Configuration
from open_lisa.repositories.commands_repository import CommandsRepository
from time import sleep
from threading import Thread

MOCK_RS232_CONFIG = RS232Configuration(port="COM4")
LOCALHOST = "127.0.0.1"
SERVER_PORT = 8080
MOCK_IMAGE_PATH = "data_test/clibs/mock_img.jpg"


def start_server():
    load_config(env="test")
    server = OpenLISA(mode="TCP", listening_port=8080,
                      rs232_config=MOCK_RS232_CONFIG)
    server._shutdown_after_next_client_connection = True
    server.start()


@pytest.fixture(autouse=True)
def on_each():

    # before each
    thread = Thread(target=start_server)
    thread.start()
    sleep(0.2)  # wait server
    yield  # run test
    # after yield emulates "after each test"
    thread.join()


def test_get_instruments():

    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments = sdk.get_instruments()

    assert instruments[0]["physical_address"] == "USB0::0x0699::0x0363::C107676::INSTR"
    assert instruments[1]["physical_address"] == "CAM_ID"
    sdk.disconnect()


def test_get_instrument_commands():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments = sdk.get_instruments()
    tektronix_test = instruments[0]
    available_commands = sdk.get_instrument_commands(
        instrument_id=tektronix_test["id"])
    commands_repository = CommandsRepository()
    commands = commands_repository.get_instrument_commands(instrument_id=1)
    assert len(available_commands) > 0
    assert len(commands) > 0
    for c in commands:
        assert available_commands.__contains__(c.name)

    sdk.disconnect()


def test_get_image_from_mock_camera():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments = sdk.get_instruments()
    mocked_camera = instruments[1]
    command_result = sdk.send_command(
        instrument_id=mocked_camera["id"],
        command_invocation="get_image",
        response_format="BYTES"
    )
    image_bytes = command_result["value"]

    with open(MOCK_IMAGE_PATH, "rb") as f:
        assert image_bytes == f.read()


def test_instrument_CRUDs():
    # NOTE: needs SDK version > 0.5.5
    VALID_INSTRUMENT_CREATION_DICT = {
        "brand": "some brand",
        "model": "some model",
        "physical_address": None,
        "type": "CLIB",
        "description": "some description"
    }

    VALID_UPDATED_BRAND = "some new brand"
    VALID_INSTRUMENT_UPDATE_DICT = {
        "brand": VALID_UPDATED_BRAND
    }

    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    new_instrument = sdk.create_instrument(
        new_instrument=VALID_INSTRUMENT_CREATION_DICT, response_format="PYTHON")
    assert new_instrument["brand"] == VALID_INSTRUMENT_CREATION_DICT["brand"]

    updated_instrument = sdk.update_instrument(
        instrument_id=new_instrument["id"], updated_instrument=VALID_INSTRUMENT_UPDATE_DICT, response_format="PYTHON")
    assert new_instrument["id"] == updated_instrument["id"]
    assert updated_instrument["brand"] == VALID_INSTRUMENT_UPDATE_DICT["brand"]

    deleted_instrument = sdk.delete_instrument(
        instrument_id=new_instrument["id"], response_format="PYTHON")
    assert new_instrument["id"] == deleted_instrument["id"]

    with pytest.raises(Exception):
        sdk.get_instrument(instrument_id=deleted_instrument["id"])

    sdk.disconnect()
