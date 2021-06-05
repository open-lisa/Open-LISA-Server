import pyvisa


class Instrument:
    def __init__(self, id, brand, model):
        self.id = id
        self.brand = brand
        self.model = model
        self.status = self.check_status()

    def check_status(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        if resources.__contains__(self.id):
            return "AVAILABLE"
        else:
            return "UNAVAILABLE"
