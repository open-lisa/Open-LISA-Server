import struct

from electronic_instrument_adapter_sdk.logging import log
from ..exceptions.sdk_exception import ElectronicInstrumentAdapterException
from ..exceptions.invalid_command import InvalidCommandException

FORMAT_STRING = "string"
FORMAT_DOUBLE = "double"
FORMAT_BYTEARRAY = "bytearray"
FORMAT_INT = "int"
AVAILABLE_RESPONSE_FORMATS = [FORMAT_STRING, FORMAT_DOUBLE, FORMAT_BYTEARRAY, FORMAT_INT]

class Instrument:
  def __init__(self, id, description, brand, model, status, client_protocol) -> None:
      self.ID = id
      self.description = description
      self.brand = brand
      self.model = model
      self.status = status
      self._client_protocol = client_protocol


  def __repr__(self) -> str:
      return 'ID: {}, Description: {}, Brand: {}, Model: {}, Status: {}'.format(self.ID, self.description, self.brand, self.model, self.status)

  @staticmethod
  def from_dict(d, client_protocol):
    mandatory_keys = ['id', 'description', 'brand', 'model', 'status']
    if all(key in d for key in mandatory_keys):
      return Instrument(id=d['id'], description=d['description'], brand=d['brand'], model=d['model'], status=d['status'], client_protocol=client_protocol)
    else:
      raise ElectronicInstrumentAdapterException("missing mandatory keys ({}) in dict {}".format(mandatory_keys, d))

  def available_commands(self):
    # todo: quizas parsear el JSON aca
    return self._client_protocol.get_instrument_commands(self.ID)

  def validate_command(self, command):
    try:
      self._client_protocol.validate_command(self.ID, command)
      print("{} is OK".format(command))
    except InvalidCommandException as e:
      print(e)

  def format_response(self, response, format):
      if format == FORMAT_STRING:
        return "{}".format(response)
      if format == FORMAT_INT:
        return int.from_bytes(response, byteorder='big', signed=False)
      if format == FORMAT_DOUBLE:
        return struct.unpack('d', response)[0]
      if format == FORMAT_BYTEARRAY:
        return response

  def send(self, command, format):
    if format not in AVAILABLE_RESPONSE_FORMATS:
        raise InvalidCommandException("command '{}' ask for invalid response format type '{}'. Available formats are {}"
                                      .format(command, format, AVAILABLE_RESPONSE_FORMATS))

    response = self._client_protocol.send_command(self.ID, command)

    return self.format_response(response, format)
