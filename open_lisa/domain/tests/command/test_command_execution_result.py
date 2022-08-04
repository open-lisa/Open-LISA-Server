import base64
import pytest
from open_lisa.domain.command.command_execution_result import CommandExecutionResult
from open_lisa.domain.command.command_return import CommandReturnType
from open_lisa.utils.date import get_UTC_timestamp

MOCK_IMAGE_PATH = "data_test/clibs/mock_img.jpg"


def test_command_execution_result_should_be_init_with_CommandReturnType():
    with pytest.raises(Exception):
        CommandExecutionResult(
            timestamp_execution_start=1, type="invalid type")


def test_command_execution_result_is_created_with_a_timestamps():
    now = get_UTC_timestamp()
    result = CommandExecutionResult(
        timestamp_execution_start=now, type=CommandReturnType.VOID)
    assert isinstance(result.timestamp_execution_start, float)
    assert result.timestamp_execution_start == now
    assert isinstance(result.timestamp_execution_end, float)


def test_command_execution_result_with_void_type():
    result = CommandExecutionResult(
        timestamp_execution_start=1, type=CommandReturnType.VOID)
    assert result.value == None


def test_command_execution_result_with_string_type():
    result = CommandExecutionResult(
        timestamp_execution_start=1,
        type=CommandReturnType.STRING, raw_value="any")
    assert result.value == "any"


def test_command_execution_result_with_int_type():
    result = CommandExecutionResult(
        timestamp_execution_start=1,
        type=CommandReturnType.INT, raw_value="4")
    assert result.value == 4


def test_command_execution_result_with_float_type():
    result = CommandExecutionResult(
        timestamp_execution_start=1,
        type=CommandReturnType.FLOAT, raw_value="4.2")
    assert result.value == 4.2


def test_command_execution_result_with_bytes_type():
    with open(MOCK_IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
        result = CommandExecutionResult(
            timestamp_execution_start=1,
            type=CommandReturnType.BYTES, raw_value=image_bytes)
        assert result.value == base64.b64encode(image_bytes).decode()
        assert image_bytes == base64.b64decode(result.value)

def test_get_value_for_file_save():
    now = get_UTC_timestamp()
    void_result = CommandExecutionResult(
        timestamp_execution_start=now, type=CommandReturnType.VOID)
    assert void_result.get_value_for_file_save() == ""

    string_result = CommandExecutionResult(
        timestamp_execution_start=1,
        type=CommandReturnType.STRING, raw_value="any")
    assert string_result.get_value_for_file_save() == "any"

    int_result = CommandExecutionResult(
        timestamp_execution_start=1,
        type=CommandReturnType.INT, raw_value="4")
    assert int_result.get_value_for_file_save() == "4"

    float_result = CommandExecutionResult(
        timestamp_execution_start=1,
        type=CommandReturnType.FLOAT, raw_value="4.2")
    assert float_result.get_value_for_file_save() == "4.2"

    with open(MOCK_IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
        bytes_result = CommandExecutionResult(
            timestamp_execution_start=1,
            type=CommandReturnType.BYTES, raw_value=image_bytes)
        assert bytes_result.get_value_for_file_save() == image_bytes
