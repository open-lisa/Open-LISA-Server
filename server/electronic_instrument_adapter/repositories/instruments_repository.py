import json
import pyvisa
from electronic_instrument_adapter.instrument.instrument import Instrument
from electronic_instrument_adapter.exceptions.instrument_not_found import InstrumentNotFoundError

class InstrumentsRepository:
  def __init__(self, path) -> None:
    self._instruments = []

    # Registered instruments
    with open(path) as file:
      data = json.load(file)

      for raw_instrument in data:
        instrument = Instrument(
          raw_instrument["id"],
          raw_instrument["brand"],
          raw_instrument["model"],
          raw_instrument["description"],
          raw_instrument["command_file"]
        )
        self._instruments.append(instrument)

    # Not registered instruments
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    for resource_id in resources:
      if not self.find_one(resource_id): # Check if it is not already registered
        instrument = Instrument(
          id=resource_id,
          brand="UNKNOWN",
          model="UNKNOWN",
          description="Not registered instrument",
          command_file=None
        )
        self._instruments.append(instrument)

  def get_all(self):
    return self._instruments

  def get_all_as_json(self):
    formatted_instruments = []

    for instrument in self._instruments:
      formatted_instruments.append(instrument.as_dict())

    return json.dumps(formatted_instruments)

  def find_one(self, id):
    match = None
    for ins in self._instruments:
      if ins.id == id:
        match = ins
        break

    if not match:
      raise InstrumentNotFoundError("instrument {} not found".format(id))

    return match