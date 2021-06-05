import flask
import json


class ElectronicInstrumentAdapter:

    def __init__(self, listening_port):
        self._listening_port = listening_port
        self.instruments = self.load_instruments()

        self._app = flask.Flask(__name__)
        self._app.config["DEBUG"] = False
        self.add_url_rules()

    def start(self):
        self._app.run(host="0.0.0.0", port=self._listening_port)

    def add_url_rules(self):
        self._app.add_url_rule('/ping', 'ping', self.ping, methods=["GET"])
        # self._app.add_url_rule('/instrument', 'instrument', self.instrument, methods=["GET"])

    def load_instruments(self):
        with open('electronic_instrument_adapter/instrument/instruments.json') as file:
            data = json.load(file)

            for oscilloscope in data["oscilloscopes"]:
                print(oscilloscope)

    def ping(self):
        return "IM ALIVE"
