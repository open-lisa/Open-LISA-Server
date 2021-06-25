import json
from .message_protocol import MessageProtocol
from ..exceptions.sdk_exception import ElectronicInstrumentAdapterException
from ..exceptions.invalid_command import InvalidCommandException

SUCCESS_RESPONSE = "OK"
ERROR_RESPONSE = "ERROR"


COMMAND_GET_INSTRUMENTS = "GET_INSTRUMENTS"
COMMAND_GET_INSTRUMENT = "GET_INSTRUMENT"
COMMAND_GET_INSTRUMENT_COMMANDS = "GET_INSTRUMENT_COMMANDS"
COMMAND_VALIDATE_COMMAND = "VALIDATE_COMMAND"
COMMAND_SEND_COMMAND = "SEND_COMMAND"

class ClientProtocol:
  def __init__(self, connection):
      self._message_protocol = MessageProtocol(connection)

  def __is_valid_response(self, response):
    if response == SUCCESS_RESPONSE:
      return True
    if response == ERROR_RESPONSE:
      return False

    raise Exception("unknown response type: '{}'".format(response))

  def get_instruments(self):
    self._message_protocol.send_msg(COMMAND_GET_INSTRUMENTS)
    return json.loads(self._message_protocol.receive_msg())

  def get_instrument(self, id):
    self._message_protocol.send_msg(COMMAND_GET_INSTRUMENT)
    self._message_protocol.send_msg(id)
    response_type = self._message_protocol.receive_msg()
    if self.__is_valid_response(response_type):
      return json.loads(self._message_protocol.receive_msg())
    else:
      raise ElectronicInstrumentAdapterException(self._message_protocol.receive_msg())

  def get_instrument_commands(self, id):
    self._message_protocol.send_msg(COMMAND_GET_INSTRUMENT_COMMANDS)
    self._message_protocol.send_msg(id)
    response_type = self._message_protocol.receive_msg()
    if self.__is_valid_response(response_type):
      return json.loads(self._message_protocol.receive_msg())
    else:
      raise ElectronicInstrumentAdapterException(self._message_protocol.receive_msg())

  def validate_command(self, id, command):
    self._message_protocol.send_msg(COMMAND_VALIDATE_COMMAND)
    self._message_protocol.send_msg(id)
    self._message_protocol.send_msg(command)
    response_type = self._message_protocol.receive_msg()
    if not self.__is_valid_response(response_type):
      err = self._message_protocol.receive_msg()
      raise InvalidCommandException("command '{}' is not valid: {}".format(command, err))

  def send_command(self, id, command):
    self._message_protocol.send_msg(COMMAND_SEND_COMMAND)
    self._message_protocol.send_msg(id)
    self._message_protocol.send_msg(command)
    response_type = self._message_protocol.receive_msg()
    if self.__is_valid_response(response_type):
      return self._message_protocol.receive_msg()
    else:
      err = self._message_protocol.receive_msg()
      raise InvalidCommandException("command '{}' for instrument {} is not valid: {}".format(command, id, err))
