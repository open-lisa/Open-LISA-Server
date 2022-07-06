
import base64
from datetime import timezone, datetime
from open_lisa.domain.command.command_return import CommandReturnType


class CommandExecutionResult():
    def __init__(self, type=CommandReturnType.VOID, raw_value=None):
        assert isinstance(type, CommandReturnType)

        # UTC timestamp
        # Src: https://www.geeksforgeeks.org/get-utc-timestamp-in-python/#:~:text=Getting%20the%20UTC%20timestamp,convert%20our%20datetime%20to%20UTC.
        self.timestamp = datetime.now(
            timezone.utc).replace(tzinfo=timezone.utc).timestamp()
        self.type = type

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
            "timestamp": self.timestamp
        }
