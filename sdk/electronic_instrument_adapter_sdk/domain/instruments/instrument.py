from ..exceptions.sdk_exception import ElectronicInstrumentAdapterException
class Instrument:
  def __init__(self, id, type, brand, model, status) -> None:
      self.ID = id
      self.type = type
      self.brand = brand
      self.model = model
      self.status = status


  def __repr__(self) -> str:
      return 'ID: {}, Type: {}, Brand: {}, Model: {}, Status: {}'.format(self.ID, self.type, self.brand, self.model, self.status)

  @staticmethod
  def from_dict(d):
    mandatory_keys = ['id', 'type', 'brand', 'model', 'status']
    if all(key in d for key in mandatory_keys):
      return Instrument(id=d['id'], type=d['type'], brand=d['brand'], model=d['model'], status=d['status'])
    else:
      raise ElectronicInstrumentAdapterException("missing mandatory keys ({}) in dict {}".format(mandatory_keys, d))