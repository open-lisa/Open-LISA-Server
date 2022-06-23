import pytest
import sys
import os

from open_lisa.domain.command.clib_command import CLibCommand
from open_lisa.domain.command.command_parameter import CommandParameter, CommandParameterType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.domain.command.command_return import CommandReturn, CommandReturnType
from open_lisa.exceptions.command_execution_error import CommandExecutionError
from open_lisa.exceptions.invalid_clib_command_function_name import InvalidCLibCommandFunctionNameError
from open_lisa.exceptions.invalid_clib_command_lib_file import InvalidCLibCommandLibFileError

# Windows systems should use .dll files and Linux based systems .so files
C_LIB_EXTENSION = "dll" if sys.platform.startswith("win") else "so"

MOCK_LIB_NAME = "mock_lib.{}".format(C_LIB_EXTENSION)
MOCK_LIB_ABSOLUTE_PATH = "{}/mock_libs/{}".format(
    os.path.dirname(__file__), MOCK_LIB_NAME)

SUM_PARAMETERS = CommandParameters()
SUM_PARAMETERS.add(CommandParameter(type=CommandParameterType.INT, position=1))
SUM_PARAMETERS.add(CommandParameter(type=CommandParameterType.INT, position=2))
SUM_RETURN = CommandReturn(type=CommandReturnType.INT)

MULTIPLY_PARAMETERS = CommandParameters()
MULTIPLY_PARAMETERS.add(CommandParameter(
    type=CommandParameterType.FLOAT, position=1))
MULTIPLY_PARAMETERS.add(CommandParameter(
    type=CommandParameterType.FLOAT, position=2))
MULTIPLY_RETURN = CommandReturn(type=CommandReturnType.FLOAT)

CREATE_FILE_PARAMETERS = CommandParameters()
CREATE_FILE_PARAMETERS.add(CommandParameter(
    type=CommandParameterType.STRING, position=1))
CREATE_FILE_RETURN = CommandReturn()  # void

ECHO_PARAMETERS = CommandParameters()
ECHO_PARAMETERS.add(CommandParameter(
    type=CommandParameterType.STRING, position=1))
ECHO_RETURN = CommandReturn(type=CommandReturnType.STRING)

COPY_IMAGE_PARAMETERS = CommandParameters()
COPY_IMAGE_PARAMETERS.add(
    CommandParameter(
        type=CommandParameterType.STRING, position=1
    )
)
COPY_IMAGE_RETURN = CommandReturn(type=CommandReturnType.BYTES)


def test_clib_command_creation_returns_an_instance_of_CLibCommand():
    some_clib_command = CLibCommand(
        name="some name",
        lib_function="sum",
        lib_file_name=MOCK_LIB_ABSOLUTE_PATH
    )
    assert isinstance(some_clib_command, CLibCommand)


def test_clib_command_to_dict_should_return_only_the_lib_file_name_without_path():
    some_clib_command = CLibCommand(
        name="some name",
        lib_function="sum",
        lib_file_name=MOCK_LIB_ABSOLUTE_PATH
    )
    d = some_clib_command.to_dict(instrument_id=1)
    assert d["lib_file_name"] == MOCK_LIB_NAME


def test_execute_should_call_the_sum_function_from_the_c_lib():
    sum_clib_command = CLibCommand(
        name="a_name",
        lib_function="sum",
        lib_file_name=MOCK_LIB_ABSOLUTE_PATH,
        parameters=SUM_PARAMETERS,
        command_return=SUM_RETURN
    )
    result = sum_clib_command.execute(params_values=["1", "2"])
    assert result == 3


def test_execute_should_call_the_multiply_function_from_the_c_lib():
    multiply_clib_command = CLibCommand(
        name="a_name",
        lib_function="multiply",
        lib_file_name=MOCK_LIB_ABSOLUTE_PATH,
        parameters=MULTIPLY_PARAMETERS,
        command_return=MULTIPLY_RETURN
    )
    result = multiply_clib_command.execute(params_values=["2", "2.5"])
    assert result == 5


def test_execute_should_call_the_create_file_function_from_the_c_lib():
    create_file_clib_command = CLibCommand(
        name="a_name",
        lib_function="create_file",
        lib_file_name=MOCK_LIB_ABSOLUTE_PATH,
        parameters=CREATE_FILE_PARAMETERS,
        command_return=CREATE_FILE_RETURN
    )
    file_name = "tmpfile"
    create_file_clib_command.execute([file_name])
    assert os.path.isfile(file_name)
    os.remove(file_name)


def test_execute_should_call_the_echo_function_from_the_c_lib():
    echo_clib_command = CLibCommand(
        name="a_name",
        lib_function="echo",
        lib_file_name=MOCK_LIB_ABSOLUTE_PATH,
        parameters=ECHO_PARAMETERS,
        command_return=ECHO_RETURN
    )
    message = "i am a bit tired..."
    output = echo_clib_command.execute([message])
    assert output == message


def test_execute_should_call_the_copy_image_function_from_the_c_lib():
    copy_image_clib_command = CLibCommand(
        name="a_name",
        lib_function="copy_image",
        lib_file_name=MOCK_LIB_ABSOLUTE_PATH,
        parameters=COPY_IMAGE_PARAMETERS,
        command_return=COPY_IMAGE_RETURN
    )
    mock_image_name = "mock_img.jpg"
    mock_image_path = "{}/mock_libs/{}".format(
        os.path.dirname(__file__), mock_image_name)

    copy = copy_image_clib_command.execute([mock_image_path])
    with open(mock_image_path, "rb") as f:
        original = f.read()
    assert original == copy


def test_execute_should_call_the_copy_image_function_from_the_c_lib_and_raise_CommandExecutionError_if_img_path_is_invalid():
    copy_image_clib_command = CLibCommand(
        name="a_name",
        lib_function="copy_image",
        lib_file_name=MOCK_LIB_ABSOLUTE_PATH,
        parameters=COPY_IMAGE_PARAMETERS,
        command_return=COPY_IMAGE_RETURN
    )
    unexisting_image = "unexisting.jpg"
    mock_image_path = "{}/mock_libs/{}".format(
        os.path.dirname(__file__), unexisting_image)

    with pytest.raises(CommandExecutionError):
        copy_image_clib_command.execute([mock_image_path])


def test_invalid_function_name_exception():
    with pytest.raises(InvalidCLibCommandFunctionNameError):
        CLibCommand(
            name="a_name",
            lib_function="unexisting_sum_function",
            lib_file_name=MOCK_LIB_ABSOLUTE_PATH,
            parameters=SUM_PARAMETERS,
            command_return=SUM_RETURN
        )


def test_invalid_function_name_exception():
    with pytest.raises(InvalidCLibCommandLibFileError):
        CLibCommand(
            name="a_name",
            lib_function="sum",
            lib_file_name="unexisting.dll",
            parameters=SUM_PARAMETERS,
            command_return=SUM_RETURN
        )
