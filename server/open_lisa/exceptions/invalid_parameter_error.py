from .base_exception import OpenLISAException

class InvalidParameterError(OpenLISAException):
    """
    Raised when command exist but format is incorrect
    """
    def __init__(self, position, correct_format, example):
        self.position = position
        self.correct_format = correct_format
        self.example = example
        message = "parameter in position {} has an invalid format, correct format is {}, ie: {}.".format(position, correct_format, example)
        super().__init__(message)
