from .base_exception import OpenLISAException


class InvalidSCPISyntaxForCommandParameters(OpenLISAException):
    """
    Raised when a SCPI Command is initialized with invalid SCPI Syntax for the parameters provided
    """

    def __init__(self, syntax, placeholders_amount):
        message = "SCPI syntax '{}' is invalid, it should have {} placeholder(s)".format(
            syntax, placeholders_amount)
        super().__init__(message)
