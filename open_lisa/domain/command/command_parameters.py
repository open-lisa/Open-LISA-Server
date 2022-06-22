from open_lisa.domain.command.command_parameter import CommandParameter, CommandParameterType
from open_lisa.exceptions.invalid_amount_parameters_error import InvalidAmountParametersError


class CommandParameters():
    def __init__(self):
        self._parameters = []

    def add(self, command):
        assert isinstance(command, CommandParameter)
        self._parameters.append(command)
        self.__sort_parameters_by_position()

    @property
    def amount(self):
        return len(self._parameters)

    def validate_parameters_values(self, params_values=[]):
        if len(params_values) != len(self._parameters):
            raise InvalidAmountParametersError(
                sent=len(params_values), required=len(self._parameters))

        for param in self._parameters:
            param_value = params_values[param.position - 1]
            param.validate_value(param_value)

    @staticmethod
    def from_dict(parameters_dict):
        parameters = CommandParameters()
        for pd in parameters_dict:
            parameters.add(CommandParameter.from_dict(pd))
        return parameters

    def to_dict(self):
        return [
            param.to_dict() for param in self._parameters
        ]

    def parameters_values_to_c_function_arguments(self, params_values=[]):
        function_arguments = []
        for param in self._parameters:
            param_value = params_values[param.position - 1]
            param_ctype = param.to_ctype()
            casted_value = param.validate_value(param_value)
            ctype_value = \
                casted_value.encode() if param.type == CommandParameterType.STRING else casted_value
            function_arguments.append(
                param_ctype(ctype_value))

        return function_arguments

    def __sort_parameters_by_position(self):
        self._parameters.sort(key=lambda param: param.position)
