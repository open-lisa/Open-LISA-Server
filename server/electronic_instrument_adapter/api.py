import flask
import json

from .instrument.oscilloscope.oscilloscope import Oscilloscope


class ElectronicInstrumentAdapter:

    def __init__(self, listening_port):
        self._listening_port = listening_port
        self._instruments = self.load_instruments()

        for instrument in self._instruments:
            print(instrument)

        self._app = flask.Flask(__name__)
        self._app.config["DEBUG"] = False
        self.add_url_rules()

    def start(self):
        self._app.run(host="0.0.0.0", port=self._listening_port)

    def add_url_rules(self):
        self._app.add_url_rule('/ping', 'ping', self.ping, methods=["GET"])
        self._app.add_url_rule('/instrument', 'instrument', self.instrument, methods=["GET"])

    def load_instruments(self):
        instruments = []
        with open('electronic_instrument_adapter/instrument/instruments.json') as file:
            data = json.load(file)

            for osc in data["oscilloscopes"]:
                instruments.append(Oscilloscope(osc['id'], osc['brand'], osc['model']))

        return instruments

    def ping(self):
        return "IM ALIVE"

    def instrument(self):
        self._instruments = self.load_instruments()
        response = []

        for instrument in self._instruments:
            response.append(instrument.__dict__)

        resp = flask.Response(json.dumps(response))
        resp.headers['Content-Type'] = 'application/json'
        return resp


