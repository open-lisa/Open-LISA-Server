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

    def start(self):
        while True:
            print("Waiting commands ...")
            time.sleep(10)
