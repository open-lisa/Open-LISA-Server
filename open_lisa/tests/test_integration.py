import pytest
import os
import json
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
COMMANDS_JSON_PATH = "{}/tektronix_test_commands.json".format(
    os.path.dirname(__file__))
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
    commands = tektronix_test.available_commands()
    with open(COMMANDS_JSON_PATH) as file:
        commands_dict = json.load(file)

    for command_name in commands_dict.keys():
        assert commands.__contains__(command_name)
    sdk.disconnect()


def test_get_image_from_mock_camera():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments = sdk.list_instruments()
    mocked_camera = instruments[1]
    image_bytes = mocked_camera.send("get_image", "bytes")

    with open(MOCK_IMAGE_PATH, "rb") as f:
        assert image_bytes == f.read()
