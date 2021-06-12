from .tektronix_tds1002b import Tektronix_TDS1002B


def OscilloscopeFactory(id):
    oscilloscopes = {
        "USB0::0x0699::0x0363::C107676::INSTR": Tektronix_TDS1002B,
    }

    return oscilloscopes[id](id)