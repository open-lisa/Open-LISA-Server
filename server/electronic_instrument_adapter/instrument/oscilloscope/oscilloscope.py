from ..instrument import Instrument


class Oscilloscope(Instrument):
    def __init__(self, id, brand, model):
        super(Oscilloscope, self).__init__(id, brand, model)
        self.type = "oscilloscope"

    def __str__(self):
        return "Oscilloscope:\n\tBrand  : {}\n\tModel  : {}\n\tID     : {}\n\tStatus : {}".format(
            self.brand,
            self.model,
            self.id,
            self.check_status())
