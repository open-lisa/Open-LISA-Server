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
        self._app.add_url_rule('/instrument', endpoint='instruments', view_func=self.instruments, methods=["GET"])
        self._app.add_url_rule('/instrument/<id>', endpoint='instrument', view_func=self.instrument, methods=["GET"])


    def load_instruments(self):
        instruments = []
        with open('electronic_instrument_adapter/instrument/instruments.json') as file:
            data = json.load(file)

            for osc in data["oscilloscopes"]:
                instruments.append(Oscilloscope(osc['id'], osc['brand'], osc['model']))

        return instruments

    def ping(self):
        return "IM ALIVE"

    def instruments(self):
        self._instruments = self.load_instruments()
        response = []

        for instrument in self._instruments:
            response.append(instrument.__dict__)

        resp = flask.Response(json.dumps(response))
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def instrument(self, id):
        resp = flask.Response(json.dumps({"msg": "instrument not found"}))
        resp.status_code = 404

        self._instruments = self.load_instruments()
        for instrument in self._instruments:
            if instrument.id == id:
                resp = flask.Response(json.dumps(instrument.__dict__))
                resp.status_code = 200

        resp.headers['Content-Type'] = 'application/json'
        return resp



