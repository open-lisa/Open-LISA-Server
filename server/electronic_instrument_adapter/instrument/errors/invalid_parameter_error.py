class InvalidParameterError(Exception):
    def __init__(self, position, correct_format, example):
        self.position = position
        self.correct_format = correct_format
        self.example = example
