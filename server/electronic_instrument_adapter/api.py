import json
import time

from .instrument.instrument import Instrument


class ElectronicInstrumentAdapter:

    def __init__(self, listening_port):
        self._listening_port = listening_port
        self._instruments = []

        self.load_instruments()
        print("Instruments List: ******************************")
        for instrument in self._instruments:
            print(instrument)
        print("***************** ******************************")

        # todo: definir nuevo protocolo con socket o USB, no more Flask

    def load_instruments(self):
        self._instruments = []
        with open('electronic_instrument_adapter/instrument/instruments.json') as file:
            data = json.load(file)

            for raw_instrument in data:
                instrument = Instrument(
                    raw_instrument["id"],
                    raw_instrument["brand"],
                    raw_instrument["model"],
                    raw_instrument["description"]
                )
                self._instruments.append(instrument)

    def get_instruments(self):
        formatted_instruments = []

        for instrument in self._instruments:
            formatted_instruments.append(instrument.as_dict())

        return json.dumps(formatted_instruments)

    def get_instrument(self, instrument_id):
        for instrument in self._instruments:
            if instrument.id == instrument_id:
                return instrument.as_dict()

        return None

    def get_instrument_commands(self, instrument_id):
        # todo: completar
        pass

    def send_command(self, command):
        # todo: completar
        pass

    def start(self):
        while True:
            print("Waiting commands ...")
            print("Instruments:")
            print(self.get_instruments())
            print("Instrument example:")
            print(self.get_instrument("USB0::0x0699::0x0363::C107676::INSTR"))
            time.sleep(10)
