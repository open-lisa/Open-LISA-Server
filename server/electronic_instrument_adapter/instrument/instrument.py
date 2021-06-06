import pyvisa


def InstrumentFactory(type, id, brand, model):
    if type == "oscilloscope":
        from .oscilloscope.factory import OscilloscopeFactory
        return OscilloscopeFactory(id, brand, model)


class Instrument:
    def __init__(self, id, brand, model):
        self.id = id
        self.brand = brand
        self.model = model
        self.device = None
        self.status = "UNAVAILABLE"

        self.set_status()

    def set_status(self):
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        if resources.__contains__(self.id):
            self.device = rm.open_resource(self.id)
            self.status = "AVAILABLE"
        else:
            self.status = "UNAVAILABLE"


class Oscilloscope(Instrument):
    def __init__(self, id, brand, model):
        super(Oscilloscope, self).__init__(id, brand, model)
        self.type = "oscilloscope"
        self.configuration = OscilloscopeConfiguration()
        if self.status == "AVAILABLE":
            self.set_initial_configuration()

    def __str__(self):
        return "Oscilloscope:\n\t" \
               "Brand  : {}\n\t" \
               "Model  : {}\n\t" \
               "ID     : {}\n\t" \
               "Status : {}".format(
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
            "configuration": {
                "volts_scale": self.configuration.volts_scale,
                "time_scale": self.configuration.time_scale
            }
        }

    def configuration_as_dict(self):
        return {
            "id": self.id,
            "configuration": {
                "volts_scale": self.configuration.volts_scale,
                "time_scale": self.configuration.time_scale
            }
        }

    def set_initial_configuration(self):
        raise Exception("NotImplementedException")

    # General purpose oscilloscope primitives

    def clear_status(self):
        raise Exception("NotImplementedException")

    def reset_settings(self):
        raise Exception("NotImplementedException")

    def get_identification(self):
        raise Exception("NotImplementedException")

    # Channel configuration primitives

    def set_channel_probe(self, channel, probe):
        raise Exception("NotImplementedException")

    # Timebase primitives

    def set_timebase_scale(self, seconds):
        raise Exception("NotImplementedException")

    def set_timebase_mode(self, mode):
        raise Exception("NotImplementedException")

    def set_timebase_x_channel(self, channel):
        raise Exception("NotImplementedException")

    def set_timebase_y_channel(self, channel):
        raise Exception("NotImplementedException")

    # Volts primitives

    def set_volts_scale(self, channel, volts_scale):
        self.device.write('CH' + str(channel) + ':VOLts ' + str(volts_scale))

    # Acquisitions primitives

    def get_is_in_acquisitions_state(self):
        raise Exception("NotImplementedException")

    def stop_acquisitions(self):
        raise Exception("NotImplementedException")


class OscilloscopeConfiguration:
    def __init__(self, volts_scale=5, time_scale=0.000500):
        self.volts_scale = volts_scale  # in volts
        self.time_scale = time_scale    # in seconds
