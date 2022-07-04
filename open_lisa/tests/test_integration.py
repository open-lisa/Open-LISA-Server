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
    instruments = sdk.list_instruments()

    assert instruments[0].ID == "USB0::0x0699::0x0363::C107676::INSTR"
    assert instruments[1].ID == "CAM_ID"
    sdk.disconnect()


def test_get_instrument_commands():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments = sdk.list_instruments()
    tektronix_test = instruments[0]
    available_commands = tektronix_test.available_commands()
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
    instruments = sdk.list_instruments()
    mocked_camera = instruments[1]
    image_bytes = mocked_camera.send("get_image", "bytes")

    with open(MOCK_IMAGE_PATH, "rb") as f:
        assert image_bytes == f.read()
