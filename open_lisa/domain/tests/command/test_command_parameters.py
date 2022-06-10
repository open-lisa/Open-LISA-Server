import pytest
from open_lisa.domain.command.command_parameter import CommandParameter, CommandParameterType
from open_lisa.domain.command.command_parameters import CommandParameters
from open_lisa.exceptions.invalid_amount_parameters_error import InvalidAmountParametersError
from open_lisa.exceptions.invalid_command_parameter_value_error import InvalidCommandParameterValueError


some_command_parameter = CommandParameter(
    type=CommandParameterType.INT, position=1, description="some useful description")
some_int_value = 1


def test_command_parameters_should_be_ordered_by_position():
    params = CommandParameters()
    second_param = CommandParameter(
        type=CommandParameterType.FLOAT, position=2, description="meaninful description")
    first_param = CommandParameter(
        type=CommandParameterType.INT, position=1, description="other description")
    params.add(second_param)
    assert second_param == params._parameters[0]
    params.add(first_param)
    assert first_param == params._parameters[0]
    assert second_param == params._parameters[1]


def test_raises_exception_if_try_to_add_something_that_is_not_a_CommandParameter():
    with pytest.raises(AssertionError):
        params = CommandParameters()
        params.add(command="invalid command parameter")


def test_validate_parameters_values_should_raise_InvalidAmountParametersError_if_parameters_values_amount_is_different_from_parameters_required_amount():
    with pytest.raises(InvalidAmountParametersError):
        params = CommandParameters()
        params.add(command=some_command_parameter)
        params.validate_parameters_values(params_values=[])

    with pytest.raises(InvalidAmountParametersError):
        params = CommandParameters()
        params.add(command=some_command_parameter)
        params.validate_parameters_values(
            params_values=[some_int_value, some_int_value])


def test_validate_parameters_values_should_not_raise_if_parameters_values_sent_are_equals_thant_required():
    try:
        params = CommandParameters()
        params.add(command=some_command_parameter)
        params.validate_parameters_values(params_values=[some_int_value])
    except InvalidAmountParametersError:
        pytest.fail("unexpected InvalidAmountParametersError")


def test_validate_parameters_values_should_raise_if_any_param_has_an_invalid_value():
    with pytest.raises(InvalidCommandParameterValueError):
        params = CommandParameters()
        params.add(command=some_command_parameter)
        params.validate_parameters_values(
            params_values=["a string is an invalid float"])

    with pytest.raises(InvalidCommandParameterValueError):
        params = CommandParameters()
        params.add(command=some_command_parameter)
        params.validate_parameters_values(
            params_values=[1.5])
