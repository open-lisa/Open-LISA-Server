
import base64

from open_lisa.domain.command.command_return import CommandReturnType
from open_lisa.utils.date import get_UTC_timestamp


class CommandExecutionResult():
    def __init__(self, timestamp_execution_start, type=CommandReturnType.VOID, raw_value=None):
        assert isinstance(type, CommandReturnType)

        self.timestamp_execution_end = get_UTC_timestamp()
        self.type = type
        self.timestamp_execution_start = timestamp_execution_start

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

    def get_value_for_file_save(self):
        if self.type == CommandReturnType.VOID:
            return ""
        elif self.type == CommandReturnType.STRING:
            return str(self.value)
        elif self.type == CommandReturnType.INT:
            return str(self.value)
        elif self.type == CommandReturnType.FLOAT:
            return str(self.value)
        elif self.type == CommandReturnType.BYTES:
            # decode and return raw bytes
            return base64.b64decode(self.value)

    def to_dict(self):
        return {
            "type": str(self.type),
            "value": self.value,
            "timestamp_execution_start":  self.timestamp_execution_start,
            "timestamp_execution_end": self.timestamp_execution_end,
        }
