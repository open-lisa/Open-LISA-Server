from open_lisa.domain.command.command_parameter import CommandParameter
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

    def __sort_parameters_by_position(self):
        self._parameters.sort(key=lambda param: param.position)
