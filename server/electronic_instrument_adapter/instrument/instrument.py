import json

import pyvisa
from .constants import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE


class Instrument:
    def __init__(self, id, brand, model, description):
        self.id = id
        self.brand = brand
        self.model = model
        self.description = description
        self.device = None
        self.status = INSTRUMENT_STATUS_UNAVAILABLE
        self.commands_map = None
        self.load_commands()

        self.set_status()

    def load_commands(self):
        with open('electronic_instrument_adapter/instrument/specs/{}_{}_cmd.json'.format(
                self.brand, self.model)) as file:
            self.commands_map = json.load(file)

    def set_status(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        if resources.__contains__(self.id):
            self.device = rm.open_resource(self.id)
            self.status = INSTRUMENT_STATUS_AVAILABLE
        else:
            self.device = None
            self.status = INSTRUMENT_STATUS_UNAVAILABLE

    def __str__(self):
        return "{}\n\t" \
               "Brand  : {}\n\t" \
               "Model  : {}\n\t" \
               "ID     : {}\n\t" \
               "Status : {}".format(
            self.description,
            self.brand,
            self.model,
            self.id,
            self.status)

    def as_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "status": self.status,
            "description": self.description
        }
