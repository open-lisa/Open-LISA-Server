import Open_LISA_SDK
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt
from timeit import default_timer as timer


def main():
    start_all = timer()

    sdk = Open_LISA_SDK.SDK()

    start = timer()
    sdk.connect_through_RS232()
    end = timer()
    timer_connection = end - start

    start = timer()
    instruments = sdk.list_instruments()
    end = timer()
    timer_list_instruments = end - start

    osc_tds1002b = None
    for i in instruments:
        if i.ID == "USB0::0x0699::0x0363::C107676::INSTR":
            osc_tds1002b = i

    if osc_tds1002b:
        start = timer()
        osc_tds1002b.send("set_waveform_source_ch1")
        end = timer()
        timer_set_command_1 = end - start

        start = timer()
        osc_tds1002b.send("set_waveform_bytes_width_1")
        end = timer()
        timer_set_command_2 = end - start

        start = timer()
        osc_tds1002b.send("set_waveform_encoding_rpbinary")
        end = timer()
        timer_set_command_3 = end - start

        Volts = np.empty(0)
        start = timer()
        ymult = float(osc_tds1002b.send("get_waveform_vertical_scale_factor"))
        end = timer()
        timer_get_command_1 = end - start

        start = timer()
        yzero = float(osc_tds1002b.send("get_waveform_conversion_factor"))
        end = timer()
        timer_get_command_2 = end - start

        start = timer()
        yoff = float(osc_tds1002b.send("get_waveform_vertical_offset"))
        end = timer()
        timer_get_command_3 = end - start

        start = timer()
        xincr = float(osc_tds1002b.send("get_waveform_horizontal_sampling_interval"))
        end = timer()
        timer_get_command_4 = end - start

        start = timer()
        data = osc_tds1002b.send("get_waveform_data")
        end = timer()
        timer_get_waveform_data = end - start

        headerlen = 2 + int(data[1])
        header = data[:headerlen]
        ADC_wave = data[headerlen:-1]
        ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))
        Volts = np.append(Volts, (ADC_wave - yoff) * ymult + yzero)
        Time = np.arange(0, xincr * len(Volts), xincr)

        start_plot = timer()
        plt.figure(figsize=(20, 10))
        plt.plot(Time, Volts)
        plt.grid()
        plt.xlabel("Time")
        plt.ylabel("Voltage [V]")
        end_plot = timer()
        timer_plot = end_plot - start_plot

        end_all = timer()

        print("timer_connection: {} sec".format(timer_connection))
        print("timer_list_instruments: {} sec".format(timer_list_instruments))
        print("timer_set_command_1: {} sec".format(timer_set_command_1))
        print("timer_set_command_2: {} sec".format(timer_set_command_2))
        print("timer_set_command_3: {} sec".format(timer_set_command_3))
        print("timer_get_command_1: {} sec".format(timer_get_command_1))
        print("timer_get_command_2: {} sec".format(timer_get_command_2))
        print("timer_get_command_3: {} sec".format(timer_get_command_3))
        print("timer_get_command_4: {} sec".format(timer_get_command_4))
        print("timer_get_waveform_data: {} sec".format(timer_get_waveform_data))

        print("timer_plot: {} sec".format(timer_plot))

        print("total summarized time: {} sec".format(timer_connection + timer_list_instruments + timer_set_command_1
                                                     + timer_set_command_2 + timer_set_command_3 + timer_get_command_1
                                                     + timer_get_command_2 + timer_get_command_3 + timer_get_command_4
                                                     + timer_get_waveform_data + timer_plot))

        print("total execution time: {} sec".format(end_all - start_all))
        plt.show()
    else:
        print("Oscilloscope TDS1002B not found")


if __name__ == "__main__":
    main()
