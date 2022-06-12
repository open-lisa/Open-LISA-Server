import pytest
from open_lisa.domain.command.command_parameter import CommandParameter, CommandParameterType

from open_lisa.exceptions.invalid_command_parameter_value_error import InvalidCommandParameterValueError


some_float_command_parameter = CommandParameter(
    type=CommandParameterType.FLOAT, position=1, description="some useful description")
some_int_command_parameter = CommandParameter(
    type=CommandParameterType.INT, position=1, description="some useful description")
some_string_command_parameter = CommandParameter(
    type=CommandParameterType.STRING, position=1, description="some useful description")

some_string_value = "string value"
some_int_value = 1
some_float_value = 2.6


def test_validate_value_for_a_float_command_parameter():
    some_float_command_parameter.validate_value(
        value=some_int_value)  # an int value is a valid float paramater value

    with pytest.raises(InvalidCommandParameterValueError):
        some_float_command_parameter.validate_value(value=some_string_value)


def test_validate_value_for_a_int_command_parameter():
    with pytest.raises(InvalidCommandParameterValueError):
        some_int_command_parameter.validate_value(value=some_float_value)

    with pytest.raises(InvalidCommandParameterValueError):
        some_int_command_parameter.validate_value(value=some_string_value)


def test_validate_value_for_a_string_command_parameter():
    # numbers are valid string parameters
    some_string_command_parameter.validate_value(value=some_float_value)
    some_string_command_parameter.validate_value(value=some_int_value)
