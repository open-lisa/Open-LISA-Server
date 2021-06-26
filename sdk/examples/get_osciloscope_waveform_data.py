import electronic_instrument_adapter_sdk
import numpy as np
from struct import unpack
import pylab

# Define server config
sdk = electronic_instrument_adapter_sdk.EIA("127.0.0.1", 8080)

# List instruments
instruments = sdk.list_instruments()
osc_tds1002b = None
for i in instruments:
  if i.id == "USB0::0x0699::0x0363::C107676::INSTR":
    osc_tds1002b = i

if osc_tds1002b:
  osc_tds1002b.send("set_waveform_source_ch1")
  osc_tds1002b.send("set_waveform_bytes_width_1")
  osc_tds1002b.send("set_waveform_encoding_rpbinary")
  Volts = np.empty(0)
  ymult = float(osc_tds1002b.send("get_waveform_vertical_scale_factor"))
  yzero = float(osc_tds1002b.send("get_waveform_conversion_factor"))
  yoff = float(osc_tds1002b.send("get_waveform_vertical_offset"))
  xincr = float(osc_tds1002b.send("get_waveform_horizontal_sampling_interval"))

  data = osc_tds1002b.send("get_waveform_data").encode()

  headerlen = 2 + int(data[1])
  header = data[:headerlen]
  ADC_wave = data[headerlen:-1]
  ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))
  Volts = np.append(Volts, (ADC_wave - yoff) * ymult + yzero)
  Time = np.arange(0, xincr * len(Volts), xincr)

  pylab.figure(figsize=(20,10))
  pylab.plot(Time, Volts)
  pylab.show()

else:
  print("Oscilloscope TDS1002B not found")