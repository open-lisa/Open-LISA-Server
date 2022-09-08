import os
import sys
import pytest
import Open_LISA_SDK


from open_lisa.api.api import OpenLISA
from open_lisa.config.config import load_config
from open_lisa.protocol.rs232_configuration import RS232_Configuration
from open_lisa.repositories.commands_repository import CommandsRepository
from time import sleep
from threading import Thread

# Update this comment when necessary
# NOTE: tested with version 0.7.7 of Open_LISA_SDK

MOCK_RS232_CONFIG = RS232_Configuration(port="COM4")
LOCALHOST = "127.0.0.1"
SERVER_PORT = 8081
MOCK_IMAGE_PATH = "data_test/clibs/mock_img.jpg"

CURR_TEST_FILE_BYTES = None
with open(__file__, "rb") as f:
    CURR_TEST_FILE_BYTES = f.read()

server = None


def start_server():
    load_config(env="test")
    server = OpenLISA(mode="TCP", listening_port=SERVER_PORT,
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


def connect_sdk() -> Open_LISA_SDK.SDK:
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    return sdk


def test_get_instruments():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments = sdk.get_instruments()

    assert instruments[0]["physical_address"] == "USB0::0x0699::0x0363::C107676::INSTR"

    # CLIB instruments has no physical address
    assert instruments[1]["physical_address"] == None
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

    sdk.disconnect()


def test_get_image_from_mock_camera_and_save_in_server():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    instruments = sdk.get_instruments()
    mocked_camera = instruments[1]
    remote_file_name = "remote.jpg"
    remote_file_path = "sandbox/" + remote_file_name
    command_result = sdk.send_command(
        instrument_id=mocked_camera["id"],
        command_invocation="get_image",
        response_format="BYTES",
        command_result_output_file=remote_file_path
    )

    assert command_result == None

    local_file_path = "./tmp.jpg"
    sdk.get_file(remote_file_path, local_file_path)

    with open(local_file_path, "rb") as f:
        get_file_returned = f.read()

    with open(MOCK_IMAGE_PATH, "rb") as f:
        assert get_file_returned == f.read()

    # clean up
    os.remove(local_file_path)
    sdk.delete_file(remote_file_path)
    sdk.disconnect()


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


def test_filesystem_manage():
    sdk = connect_sdk()
    root_folder = "sandbox"
    remote_file_sub_path = "/remote_test_integration.py"
    remote_file_path = root_folder + remote_file_sub_path

    sdk.send_file(__file__, remote_file_path)

    local_file_path = "./tmp.py"
    sdk.get_file(remote_file_path, local_file_path)

    with open(local_file_path, "rb") as f:
        assert f.read() == CURR_TEST_FILE_BYTES

    os.remove(local_file_path)

    sdk.delete_file(remote_file_path)

    sdk.disconnect()


def test_create_clib_instrument_command():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)
    lib_file_name = "libpixelflyqe.dll"
    if sys.platform.startswith('win'):
        lib_file_name = lib_file_name.replace(".dll", "_x86.dll")
    VALID_INSTRUMENT_COMMAND_DICT = {
        "name": "activate_smoke",
        "command": "get_image",
        "instrument_id": 1,
        "type": "CLIB",
        "description": "Generate smoke for indicated period of time in seconds",
        "params": [],
        "return": {
                "type": "VOID",
                "description": ""
        },
        "metadata": {
            "lib_file_name": lib_file_name
        }
    }

    new_instrument_command = sdk.create_instrument_command(
        new_command=VALID_INSTRUMENT_COMMAND_DICT, response_format="PYTHON")

    VALID_INSTRUMENT_COMMAND_DICT["id"] = new_instrument_command["id"]
    assert new_instrument_command == VALID_INSTRUMENT_COMMAND_DICT

    sdk.disconnect()


def test_create_scpi_instrument_command():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)

    VALID_INSTRUMENT_COMMAND_DICT = {
        "name": "activate_laser",
        "command": "ACTIVATE LASER {}",
        "instrument_id": 1,
        "type": "SCPI",
        "description": "Activate laser for indicated period of time in seconds",
        "params": [
                {
                    "position": 1,
                    "type": "INT",
                    "description": "Number of seconds for the laser be activated"
                }
        ],
        "return": {
            "type": "VOID",
            "description": ""
        },
        "metadata": None
    }

    new_instrument_command = sdk.create_instrument_command(
        new_command=VALID_INSTRUMENT_COMMAND_DICT, response_format="PYTHON")

    VALID_INSTRUMENT_COMMAND_DICT["id"] = new_instrument_command["id"]
    new_instrument_command["params"] = sorted(new_instrument_command["params"])
    VALID_INSTRUMENT_COMMAND_DICT["params"] = sorted(
        VALID_INSTRUMENT_COMMAND_DICT["params"])

    assert new_instrument_command == VALID_INSTRUMENT_COMMAND_DICT

    sdk.disconnect()


def test_delete_instrument_command():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)

    TARGET_INSTRUMENT_ID = 1
    TARGET_COMMAND_ID = 2

    instrument_commands = sdk.get_instrument_commands(TARGET_INSTRUMENT_ID)
    original_instrument_commands_size = len(instrument_commands)

    sdk.delete_instrument_command(TARGET_COMMAND_ID)
    instrument_commands = sdk.get_instrument_commands(TARGET_INSTRUMENT_ID)

    assert len(instrument_commands) == original_instrument_commands_size - 1

    sdk.disconnect()


def test_create_directory_valid():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)

    sdk.create_directory("sandbox", "pepinardovich")

    assert os.path.isdir("./data_test/sandbox/pepinardovich")

    os.rmdir("./data_test/sandbox/pepinardovich")

    sdk.disconnect()


def test_create_directory_invalid():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)

    try:
        sdk.create_directory("win32", "experience")
    except Exception as e:
        assert e.message.find("forbidden") != -1
        sdk.disconnect()
        return

    sdk.disconnect()
    assert 1 == 0


def test_delete_directory_valid():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)

    sdk.create_directory("sandbox", "pepinardovich")

    assert os.path.isdir("./data_test/sandbox/pepinardovich")

    sdk.delete_directory("sandbox/pepinardovich")

    assert not os.path.isdir("./data_test/sandbox/pepinardovich")

    sdk.disconnect()


def test_delete_directory_invalid():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)

    try:
        sdk.delete_directory("sandbox")
    except Exception as e:
        assert e.message.find("forbidden deletion") != -1
        sdk.disconnect()
        return

    sdk.disconnect()
    assert 1 == 0


def test_delete_instrument_must_delete_instrument_commands():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host=LOCALHOST, port=SERVER_PORT)

    TARGET_INSTRUMENT = 1
    instrument_commands = sdk.get_instrument_commands(TARGET_INSTRUMENT)
    assert instrument_commands is not None
    assert len(instrument_commands) > 0

    sdk.delete_instrument(TARGET_INSTRUMENT)
    try:
        instrument_commands = sdk.get_instrument_commands(TARGET_INSTRUMENT)
    except Exception as e:
        assert e.message.find("instrument not found for id 1") != 1
        sdk.disconnect()
        return

    sdk.disconnect()
    assert 1 == 0
