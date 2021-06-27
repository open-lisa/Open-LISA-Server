from electronic_instrument_adapter_sdk import EIA
from electronic_instrument_adapter_sdk.domain.exceptions.sdk_exception import ElectronicInstrumentAdapterException
import numpy as np
from struct import unpack

def list_all(host, port):
  try:
    sdk = EIA(host, port)
    return sdk.list_instruments()
  except ElectronicInstrumentAdapterException as e:
    print("SDK Error")
    print(e)

def get_instrument(host, port, id):
  try:
    sdk = EIA(host, port)
    instruments = sdk.list_instruments()
    for i in instruments:
      if i.ID == id:
        return i

    return None
  except ElectronicInstrumentAdapterException as e:
    print("SDK Error")
    print(e)

def list_instrument_commands(host, port, id):
  try:
    instrument = get_instrument(host, port, id)

    if instrument:
      commands = instrument.available_commands()
      for c in commands:
        print(c)
    else:
      print("instrument not found with ID {}".format(id))
  except ElectronicInstrumentAdapterException as e:
    print("SDK Error")
    print(e)

def validate_command(host, port, id, command):
  try:
    instrument = get_instrument(host, port, id)

    if instrument:
      instrument.validate_command(command)
    else:
      print("instrument not found with ID {}".format(id))
  except ElectronicInstrumentAdapterException as e:
    print("SDK Error")
    print(e)

def get_measure(host, port, id):
  try:
    instrument = get_instrument(host, port, id)
    if instrument:

      # Specific for Oscilloscope Tektronix TDS1002B
      instrument.send("set_waveform_source_ch1")
      instrument.send("set_waveform_bytes_width_1")
      instrument.send("set_waveform_encoding_rpbinary")
      Volts = np.empty(0)
      ymult = float(instrument.send("get_waveform_vertical_scale_factor"))
      yzero = float(instrument.send("get_waveform_conversion_factor"))
      yoff = float(instrument.send("get_waveform_vertical_offset"))
      xincr = float(instrument.send("get_waveform_horizontal_sampling_interval"))

      data = instrument.send("get_waveform_data")

      headerlen = 2 + int(data[1])
      header = data[:headerlen]
      ADC_wave = data[headerlen:-1]
      ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))
      Volts = np.append(Volts, (ADC_wave - yoff) * ymult + yzero)
      Time = np.arange(0, xincr * len(Volts), xincr)
      return Time, Volts
    else:
      print("instrument not found with ID {}".format(id))
  except ElectronicInstrumentAdapterException as e:
    print("SDK Error")
    print(e)