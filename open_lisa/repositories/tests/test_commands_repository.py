
import pytest
import sys
import os
from open_lisa.domain.command.clib_command import CLibCommand
from open_lisa.domain.command.command import Command
from open_lisa.domain.command.command_parameter import CommandParameter, CommandParameterType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.scpi_command import SCPICommand
from open_lisa.repositories.commands_repository import DEFAULT_C_LIBS_PATH, CommandsRepository

TMP_DB_PATH = "tmp.commands.db.json"

SET_CHANNEL_VOLTS_NAME = "set_channel_volts"
SET_CHANNEL_VOLTS_SCPI_SYNTAX = "CH{} VOLts {}"
SET_CHANNEL_VOLTS_PARAMETERS = CommandParameters()
SET_CHANNEL_VOLTS_PARAMETERS.add(CommandParameter(
    type=CommandParameterType.INT, position=1))
SET_CHANNEL_VOLTS_PARAMETERS.add(CommandParameter(
    type=CommandParameterType.FLOAT, position=2))
SET_CHANNEL_VOLTS_PARAMETERS_VALUES = [1, 5.0]
some_valid_scpi_command = SCPICommand(
    name="set_channel_volts",
    pyvisa_resource=None,
    scpi_template_syntax=SET_CHANNEL_VOLTS_SCPI_SYNTAX,
    parameters=SET_CHANNEL_VOLTS_PARAMETERS
)
some_instrument_id = 1234


# Windows systems should use .dll files and Linux based systems .so files
C_LIB_EXTENSION = "dll" if sys.platform.startswith("win") else "so"

MOCK_LIB_NAME = "mock_lib.{}".format(C_LIB_EXTENSION)
MOCK_LIB_PATH = "{}{}".format(DEFAULT_C_LIBS_PATH, MOCK_LIB_NAME)


@pytest.fixture(autouse=True)
def after_each():
    # code here is before each
    yield
    # after yield emulates "after each test"
    try:
        os.remove(TMP_DB_PATH)
        os.remove("{}.lock".format(TMP_DB_PATH))
    except:
        pass

# Begin JSONRepository tests


def test_CommandsRepository_initialization_should_create_json_file():
    CommandsRepository(commands_db_path=TMP_DB_PATH)
    assert os.path.isfile(TMP_DB_PATH)


def test_add_scpi_command_should_add_an_entry_in_json_file():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    command_id = repo.add(command=some_valid_scpi_command,
                          instrument_id=some_instrument_id)

    entry = repo.get_by_id(command_id)
    assert entry is not None
    assert entry["instrument_id"] == some_instrument_id
    assert entry["name"] == some_valid_scpi_command.name
    assert entry["command"] == some_valid_scpi_command.command
    assert entry["description"] == some_valid_scpi_command.description
    assert entry["type"] == str(some_valid_scpi_command.type)


def test_add_scpi_command_should_do_that_get_all_returns_data():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    assert len(repo.get_all()) == 0
    repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    assert len(repo.get_all()) != 0


def test_get_existing_command_by_name():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    command = repo.get_first_by_key_value(
        key="name", value=some_valid_scpi_command.name)
    assert command is not None


def test_get_commands_of_an_instrument():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    repo.add(
        command=some_valid_scpi_command,
        instrument_id=1
    )
    assert len(repo.get_all()) == 3
    assert len(repo.get_by_key_value("instrument_id", some_instrument_id)) == 2


def test_get_not_existing_command_by_name():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    command = repo.get_first_by_key_value(
        key="name", value=some_valid_scpi_command.name)
    assert command is None


def test_update_by_id_should_update_entry():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    id = repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    new_name = "new"
    repo.update_by_id(id, {"name": new_name})
    command = repo.get_by_id(id)
    assert command["name"] == new_name


def test_update_all_should_update_entry():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    id = repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    new_name = "new"
    repo.update_all(
        {"name": some_valid_scpi_command.name},
        {"name": new_name}
    )
    command = repo.get_by_id(id)
    assert command["name"] == new_name


def test_remove_by_id():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    assert len(repo.get_all()) == 0
    command_id = repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    assert len(repo.get_all()) != 0
    repo.remove_by_id(command_id)
    assert len(repo.get_all()) == 0
# End JSONRepository tests


# Begin CommandsRepository tests
def test_get_instrument_commands_should_return_a_list_of_commands_objects():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    other_instrument_id = 999
    repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    repo.add(
        command=some_valid_scpi_command,
        instrument_id=some_instrument_id
    )
    repo.add(
        command=some_valid_scpi_command,
        instrument_id=other_instrument_id
    )

    commands = repo.get_instrument_commands(instrument_id=some_instrument_id)
    assert len(commands) == 2
    for command in commands:
        assert isinstance(command, Command)


def test_should_only_store_c_lib_filename_without_path_for_CLibCommands():
    repo = CommandsRepository(commands_db_path=TMP_DB_PATH)
    clib_command = CLibCommand(
        name="name", lib_function="sum", lib_file_name=MOCK_LIB_PATH)
    command_id = repo.add(command=clib_command,
                          instrument_id=some_instrument_id)
    command_dict = repo.get_by_id(command_id)
    assert command_dict["lib_file_name"] == MOCK_LIB_NAME
# End CommandsRepository tests
