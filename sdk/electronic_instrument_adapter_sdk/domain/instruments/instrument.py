from ..exceptions.sdk_exception import ElectronicInstrumentAdapterException
class Instrument:
  def __init__(self, id, name) -> None:
      self.ID = id
      self.name = name

  def __repr__(self) -> str:
      return 'ID: {}, Name: {}'.format(self.ID, self.name)

  @staticmethod
  def from_dict(d):
    mandatory_keys = ['id', 'name']
    if all(key in d for key in mandatory_keys):
      return Instrument(id=d['id'], name=d['name'])
    else:
      raise ElectronicInstrumentAdapterException("missing mandatory keys ({}) in dict {}".format(mandatory_keys, d))