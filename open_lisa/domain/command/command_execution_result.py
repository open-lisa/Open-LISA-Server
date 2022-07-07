
import base64

from open_lisa.domain.command.command_return import CommandReturnType
from open_lisa.utils.date import get_UTC_timestamp


class CommandExecutionResult():
    def __init__(self, timestamp_execution_begin, type=CommandReturnType.VOID, raw_value=None):
        assert isinstance(type, CommandReturnType)

        self.timestamp_execution_finish = get_UTC_timestamp()
        self.type = type
        self.timestamp_execution_begin = timestamp_execution_begin

        if type == CommandReturnType.VOID:
            self.value = None
        elif type == CommandReturnType.STRING:
            self.value = str(raw_value)
        elif type == CommandReturnType.INT:
            self.value = int(raw_value)
        elif type == CommandReturnType.FLOAT:
            self.value = float(raw_value)
        elif type == CommandReturnType.BYTES:
            # bytes are encoded in base64 in order to
            # can be represented in json format.
            # Ref: https://stackoverflow.com/questions/27837346/how-to-include-pictures-bytes-to-a-json-with-python-encoding-issue
            self.value = base64.b64encode(raw_value).decode()

    def to_dict(self):
        return {
            "type": str(self.type),
            "value": self.value,
            "timestamp_execution_begin":  self.timestamp_execution_begin,
            "timestamp_execution_finish": self.timestamp_execution_finish,
        }
