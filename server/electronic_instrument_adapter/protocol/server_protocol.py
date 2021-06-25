import json
from .message_protocol import MessageProtocol
from electronic_instrument_adapter.instrument.errors.command_not_found_error import CommandNotFoundError
from electronic_instrument_adapter.instrument.errors.invalid_amount_parameters_error import InvalidAmountParametersError
from electronic_instrument_adapter.instrument.errors.invalid_parameter_error import InvalidParameterError

SUCCESS_RESPONSE = "OK"
ERROR_RESPONSE = "ERROR"


COMMAND_GET_INSTRUMENTS = "GET_INSTRUMENTS"
COMMAND_GET_INSTRUMENT = "GET_INSTRUMENT"
COMMAND_GET_INSTRUMENT_COMMANDS = "GET_INSTRUMENT_COMMANDS"
COMMAND_VALIDATE_COMMAND = "VALIDATE_COMMAND"
COMMAND_SEND_COMMAND = "SEND_COMMAND"

ERROR_INSTRUMENT_NOT_FOUND = "instrument not found"

class ServerProtocol:
  def __init__(self, connection):
      self._message_protocol = MessageProtocol(connection)

  def get_command(self):
    return self._message_protocol.receive_msg()

  def handle_get_instruments(self, instruments):
    self._message_protocol.send_msg(instruments)

  def handle_get_instrument(self, instruments):
    id = self._message_protocol.receive_msg()
    for instrument in instruments:
      if instrument.id == id:
        self._message_protocol.send_msg(SUCCESS_RESPONSE)
        self._message_protocol.send_msg(instrument.as_dict())
        return

    self._message_protocol.send_msg(ERROR_RESPONSE)
    self._message_protocol.send_msg(ERROR_INSTRUMENT_NOT_FOUND)

  def handle_get_instrument_commands(self, instruments):
    id = self._message_protocol.receive_msg()
    for instrument in instruments:
      if instrument.id == id:
        self._message_protocol.send_msg(SUCCESS_RESPONSE)
        self._message_protocol.send_msg(json.dumps(instrument.commands_map))
        return

    self._message_protocol.send_msg(ERROR_RESPONSE)
    self._message_protocol.send_msg(ERROR_INSTRUMENT_NOT_FOUND)

  def handle_validate_command(self, instruments):
    id = self._message_protocol.receive_msg()
    command = self._message_protocol.receive_msg()
    err_msg = None
    for instrument in instruments:
      if instrument.id == id:
        try:
          instrument.validate_command(command)
        except CommandNotFoundError:
          err_msg = "Command not found"
        except InvalidAmountParametersError as e:
          err_msg = "{} Parameters has sent, but {} are required.".format(
            e.parameters_amount_sent,
            e.parameters_amount_required
          )
        except InvalidParameterError as e:
          err_msg = "Parameter in position {} has an invalid format. Correct format is {}, ie: {}.".format(
            e.position,
            e.correct_format,
            e.example
          )
        finally:
          if err_msg:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(err_msg)
            return

    self._message_protocol.send_msg(SUCCESS_RESPONSE)

  def handle_send_command(self, instruments):
    # todo, abstraer instrument not found y validacion del comando
    pass
