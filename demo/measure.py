import time
import pyvisa
import numpy as np
from struct import unpack
import pylab

rm = pyvisa.ResourceManager()
device = rm.open_resource("USB0::0x0699::0x0363::C107676::INSTR")

# Sets Channel 1 to be the waveform source data
device.write('DATa:SOUrce CH1')
# sets the number of bytes per waveform data point to 1 byte (8 bits)
device.write('DATa:WIDth 1')
# RPBinary specifies positive integer data-point representation with the most significant byte transferred first.
device.write('DATa:ENCdg RPBinary')

Volts = np.empty(0)

for i in range(5):
    # Query the vertical scale factor
    ymult = float(device.query('WFMPre:YMUlt?'))
    # Query the waveform conversion factor
    yzero = float(device.query('WFMPre:YZEro?'))
    # Query the vertical offseT
    yoff = float(device.query('WFMPre:YOFf?'))
    # Set or query the horizontal sampling interval
    xincr = float(device.query('WFMPre:XINcr?'))

    device.write('CURVE?')

    data = device.read_raw()
    print(len(data))

    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]

    ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))

    Volts = np.append(Volts, (ADC_wave - yoff) * ymult + yzero)
    print(len(Volts))

    print(type(Volts))

    time.sleep(1)


Time = np.arange(0, xincr * len(Volts), xincr)

pylab.figure(figsize=(20,10))
pylab.plot(Time, Volts)
pylab.show()
