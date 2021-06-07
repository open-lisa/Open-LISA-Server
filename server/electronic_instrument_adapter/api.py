import flask
import json

from .instrument.instrument import InstrumentFactory


class ElectronicInstrumentAdapter:

    def __init__(self, listening_port):
        self._listening_port = listening_port
        self._instruments = []

        self.load_instruments()
        print("Instruments List: ******************************")
        for instrument in self._instruments:
            print(instrument)
        print("***************** ******************************")

        self._app = flask.Flask(__name__)
        self._app.config["DEBUG"] = False
        self.add_url_rules()

    def start(self):
        self._app.run(host="0.0.0.0", port=self._listening_port)

    def add_url_rules(self):
        self._app.add_url_rule('/ping', 'ping', self.ping, methods=["GET"])
        self._app.add_url_rule('/instrument', endpoint='instruments', view_func=self.instruments, methods=["GET"])
        self._app.add_url_rule('/instrument/<id>', endpoint='instrument', view_func=self.instrument, methods=["GET"])
        self._app.add_url_rule('/instrument/oscilloscope/<id>/configuration', endpoint='oscilloscope_configuration', view_func=self.oscilloscope_configuration, methods=["POST", "GET"])

    def load_instruments(self):
        self._instruments = []
        with open('electronic_instrument_adapter/instrument/instruments.json') as file:
            data = json.load(file)

            for raw_instrument in data:
                instrument = InstrumentFactory(raw_instrument["type"], raw_instrument["id"])

                self._instruments.append(instrument)

    def ping(self):
        return "IM ALIVE"

    def instruments(self):
        self.load_instruments()
        response = []

        for instrument in self._instruments:
            response.append(instrument.as_dict())

        resp = flask.Response(json.dumps(response))
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def instrument(self, id):
        self.load_instruments()
        resp = flask.Response(json.dumps({"msg": "instrument not found"}))
        resp.status_code = 404

        for instrument in self._instruments:
            if instrument.id == id:
                resp = flask.Response(json.dumps(instrument.as_dict()))
                resp.status_code = 200

        resp.headers['Content-Type'] = 'application/json'
        return resp

    def oscilloscope_configuration(self, id):
        resp = flask.Response(json.dumps({"msg": "oscilloscope not found"}))
        resp.status_code = 404

        self.load_instruments()
        for instrument in self._instruments:
            if instrument.id == id and instrument.type == "oscilloscope":
                if flask.request.method == "GET":
                    resp = flask.Response(json.dumps(instrument.configuration_as_dict()))
                    resp.status_code = 200

        resp.headers['Content-Type'] = 'application/json'
        return resp

