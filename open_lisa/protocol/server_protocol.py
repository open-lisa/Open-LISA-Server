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
COMMAND_DISCONNECT = "DISCONNECT"


class ServerProtocol:
    def __init__(self, message_protocol):
        self._message_protocol = message_protocol

    def get_command(self):
        return self._message_protocol.receive_msg()

    def handle_get_instruments(self, instruments_repository):
        # TODO: Temporary send physical_address as id in order to be retrocompatible with SDK
        jsons_string = instruments_repository.get_all_as_json()
        list_of_dicts = json.loads(jsons_string)
        for instrument_dict in list_of_dicts:
            instrument_dict["id"] = instrument_dict["physical_address"]

        self._message_protocol.send_msg(json.dumps(list_of_dicts))

    def handle_get_instrument(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_physical_address(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            # TODO: Temporary send physical_address as id in order to be retrocompatible with SDK
            instrument_dict = instrument.to_dict()
            instrument_dict["id"] = instrument_dict["physical_address"]
            self._message_protocol.send_msg(json.dumps(instrument_dict))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_get_instrument_commands(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_physical_address(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(
                json.dumps(instrument.commands_map))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)
            return

    def handle_validate_command(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        command = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_physical_address(id)
            commands_parts = command.split(' ')
            command_name = commands_parts[0]
            command_params = \
                commands_parts[1:] if len(commands_parts) > 1 else []
            instrument.validate_command(command_name, command_params)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_send_command(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        command = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_physical_address(id)
            commands_parts = command.split(' ')
            command_name = commands_parts[0]
            command_params = \
                commands_parts[1:] if len(commands_parts) > 1 else []
            command_execution_result = instrument.send_command(
                command_name, command_params)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(
                json.dumps(command_execution_result.to_dict()))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_disconnect_command(self):
        self._message_protocol.disconnect()
