import json
from .message_protocol import MessageProtocol
from electronic_instrument_adapter.exceptions.base_exception import ElectronicInstrumentAdapterException

SUCCESS_RESPONSE = "OK"
ERROR_RESPONSE = "ERROR"


COMMAND_GET_INSTRUMENTS = "GET_INSTRUMENTS"
COMMAND_GET_INSTRUMENT = "GET_INSTRUMENT"
COMMAND_GET_INSTRUMENT_COMMANDS = "GET_INSTRUMENT_COMMANDS"
COMMAND_VALIDATE_COMMAND = "VALIDATE_COMMAND"
COMMAND_SEND_COMMAND = "SEND_COMMAND"

class ServerProtocol:
  def __init__(self, connection):
      self._message_protocol = MessageProtocol(connection)

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
    except ElectronicInstrumentAdapterException as e:
      self._message_protocol.send_msg(ERROR_RESPONSE)
      self._message_protocol.send_msg(e.message)

  def handle_get_instrument_commands(self, instruments_repository):
    id = self._message_protocol.receive_msg()
    try:
      instrument = instruments_repository.find_one(id)
      self._message_protocol.send_msg(SUCCESS_RESPONSE)
      self._message_protocol.send_msg(json.dumps(instrument.commands_map))
    except ElectronicInstrumentAdapterException as e:
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
    except ElectronicInstrumentAdapterException as e:
      self._message_protocol.send_msg(ERROR_RESPONSE)
      self._message_protocol.send_msg(e.message)

  def handle_send_command(self, instruments_repository):
    id = self._message_protocol.receive_msg()
    command = self._message_protocol.receive_msg()
    try:
      instrument = instruments_repository.find_one(id)
      result = instrument.send_command(command)
      self._message_protocol.send_msg(SUCCESS_RESPONSE)
      self._message_protocol.send_msg(json.dumps(result))
    except ElectronicInstrumentAdapterException as e:
      self._message_protocol.send_msg(ERROR_RESPONSE)
      self._message_protocol.send_msg(e.message)
