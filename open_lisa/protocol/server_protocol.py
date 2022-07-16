import json
import logging
import os

from open_lisa.repositories.instruments_repository import InstrumentRepository
from open_lisa.tests.utils import reset_databases
from .message_protocol import MessageProtocol
from open_lisa.exceptions.base_exception import OpenLISAException

SUCCESS_RESPONSE = "OK"
ERROR_RESPONSE = "ERROR"

COMMAND_GET_INSTRUMENTS = "GET_INSTRUMENTS"
COMMAND_GET_INSTRUMENT = "GET_INSTRUMENT"
COMMAND_CREATE_INSTRUMENT = "CREATE_INSTRUMENT"
COMMAND_UPDATE_INSTRUMENT = "UPDATE_INSTRUMENT"
COMMAND_DELETE_INSTRUMENT = "DELETE_INSTRUMENT"
COMMAND_GET_INSTRUMENT_COMMANDS = "GET_INSTRUMENT_COMMANDS"
COMMAND_VALIDATE_COMMAND = "VALIDATE_COMMAND"
COMMAND_SEND_COMMAND = "SEND_COMMAND"
COMMAND_DISCONNECT = "DISCONNECT"

# Only available when running in test mode
COMMAND_RESET_DATABASES = "RESET_DATABASES"


class ServerProtocol:
    def __init__(self, message_protocol):
        self._message_protocol = message_protocol

    def get_command(self):
        return self._message_protocol.receive_msg()

    def handle_get_instruments(self, instruments_repository: InstrumentRepository):
        jsons_string = instruments_repository.get_all_as_json()
        self._message_protocol.send_msg(jsons_string)

    def handle_get_instrument(self, instruments_repository: InstrumentRepository):
        id = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_id(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(json.dumps(instrument.to_dict()))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_create_instrument(self, instruments_repository: InstrumentRepository):
        new_instrument_payload = json.loads(
            self._message_protocol.receive_msg())
        try:
            new_instrument = instruments_repository.create_instrument(
                new_instrument_payload)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(
                json.dumps(new_instrument.to_dict()))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_update_instrument(self, instruments_repository: InstrumentRepository):
        id = self._message_protocol.receive_msg()
        update_instrument_payload = json.loads(
            self._message_protocol.receive_msg())
        try:
            updated_instrument = instruments_repository.update_instrument(
                id, update_instrument_payload)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(
                json.dumps(updated_instrument.to_dict()))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_delete_instrument(self, instruments_repository: InstrumentRepository):
        id = self._message_protocol.receive_msg()
        try:
            deleted_instrument = instruments_repository.delete_instrument(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(
                json.dumps(deleted_instrument.to_dict()))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_get_instrument_commands(self, instruments_repository: InstrumentRepository):
        id = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_id(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(
                json.dumps(instrument.commands_map))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)
            return

    def handle_validate_command(self, instruments_repository: InstrumentRepository):
        id = self._message_protocol.receive_msg()
        command = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_id(id)
            commands_parts = command.split(' ')
            command_name = commands_parts[0]
            command_params = \
                commands_parts[1:] if len(commands_parts) > 1 else []
            instrument.validate_command(command_name, command_params)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_send_command(self, instruments_repository: InstrumentRepository):
        id = self._message_protocol.receive_msg()
        command = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_id(id)
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

    def handle_reset_databases(self):
        env = os.environ["ENV"]
        if env == "test":
            logging.info(
                "[handle_reset_databases] - resetting databases")
            reset_databases()
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
        else:
            logging.info(
                "[handle_reset_databases] - command reset databases not supported for {} environment".format(env))
            self._message_protocol.send_msg("not supported")
