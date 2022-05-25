import json
from .message_protocol import MessageProtocol
from open_lisa.exceptions.base_exception import OpenLISAException

SUCCESS_RESPONSE = "OK"
ERROR_RESPONSE = "ERROR"

COMMAND_GET_INSTRUMENTS = "GET_INSTRUMENTS"
COMMAND_GET_INSTRUMENT = "GET_INSTRUMENT"
COMMAND_GET_INSTRUMENT_COMMANDS = "GET_INSTRUMENT_COMMANDS"
COMMAND_VALIDATE_COMMAND = "VALIDATE_COMMAND"
COMMAND_SEND_COMMAND = "SEND_COMMAND"


class ServerProtocol:
    def __init__(self, message_protocol):
        self._message_protocol = message_protocol

    def get_command(self):
        return self._message_protocol.receive_msg()

    def handle_get_instruments(self, instruments_repository):
        self._message_protocol.send_msg(instruments_repository.get_all_as_json())

    def handle_get_instrument(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.find_one(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(instrument.as_dict())
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_get_instrument_commands(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.find_one(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(json.dumps(instrument.commands_map))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)
            return

    def handle_validate_command(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        command = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.find_one(id)
            instrument.validate_command(command)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_send_command(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        command = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.find_one(id)
            result = instrument.send_command(command)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            format = type(result).__name__
            encode = False
            if format == "str":
                encode = True
            self._message_protocol.send_msg(format)
            self._message_protocol.send_msg(result, encode=encode)
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)
