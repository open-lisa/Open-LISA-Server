import json
import logging
from .oscilloscope import Oscilloscope


class Tektronix_TDS1002B(Oscilloscope):
    def __init__(self, id):
        super().__init__(id, "Tektronix", "TDS1002B")
        with open('electronic_instrument_adapter/instrument/oscilloscope/configs/oscilloscope_tektronix_tds1002b.json') as file:
            cfg = json.load(file)
            self._available_acquisition_modes = [mode["value"] for mode in cfg["acquisition"]["mode"]]
            self._available_average_acquisition_mode_samples_amount =[amount["value"] for amount in cfg["acquisition"]["average_mode_samples_amount"]]
            self._available_timebase_modes = [mode["value"] for mode in cfg["timebase"]["mode"]]
            self._available_channels = [channel["value"] for channel in cfg["channels"]["amount"]]
            self._available_channel_attenuations_factors = [attenuation["value"] for attenuation in cfg["channels"]["attenuation_factors"]]

    def set_initial_configuration(self):
        self.configuration.volts_scale = 0.5
        self.configuration.time_scale = 0.000200

        self.stop_acquisitions()
        self.clear_status()

        self.set_channel_probe("CH1", 1)
        self.set_channel_probe("CH2", 1)

        self.set_channel_volts_scale("CH1", self.configuration.volts_scale)
        self.set_channel_volts_scale("CH2", self.configuration.volts_scale)

        self.set_timebase_mode("YT")

        self.set_timebase_x_channel("CH1")
        self.set_timebase_y_channel("CH2")

        self.set_timebase_scale(self.configuration.time_scale)

        self.set_acquisition_mode("AVErage")
        self.set_average_acquisition_mode_samples_amount("16")

    def clear_status(self):
        self.device.write("*CLS")

    def reset_settings(self):
        self.device.write("*RST")

    def get_identification(self):
        return self.device.query("*IDN?")

    def stop_acquisitions(self):
        self.device.write("ACQuire:STATE STOP")

    def get_is_in_acquisitions_state(self):
        return self.device.query("*OPC?") == 1



    """
        BEGIN CHANNEL PRIMITIVES
    """
    def set_channel_volts_scale(self, channel, volts_scale):
        """
            Sets the vertical gain of the specified channel
        """
        channel = str(channel)
        volts_scale = str(volts_scale)
        if channel not in self._available_channels:
            logging.warning("Not supported channel {}, supported are {}".format(channel, self._available_channels))
            return

        self.device.write('CH{}:VOLts {}'.format(channel, volts_scale))

    def set_channel_probe(self, channel, probe):
        """
            Sets the attenuation factor of the specified channel or voltage probes.
        """
        channel = str(channel)
        probe = str(probe)
        if channel not in self._available_channels:
            logging.warning("Not supported channel {}, supported are {}".format(channel, self._available_channels))
            return

        if probe not in self._available_channel_attenuations_factors:
            logging.warning("Not supported attenuation factor {}, supported are".format(probe, self._available_channel_attenuations_factors))
            return

        self.device.write("{}:PRObe {}".format(channel, probe))
    """
        END CHANNEL PRIMITIVES
    """



    """
        BEGIN TIMEBASE PRIMITIVES
    """
    def set_timebase_scale(self, seconds):
        """
            Sets the time per division for the main time base. The acceptable values are
            in a 1–2.5–5 sequence. Other values are forced to the closest acceptable value.
        """
        seconds = str(seconds)
        self.device.write('HORizontal:MAIn:SCAle {}'.format(seconds)))

    def set_timebase_mode(self, mode):
        """
            Sets the oscilloscope display format.
        """
        mode = str(mode)
        if mode in self._available_timebase_modes:
            self.device.write('DISplay:FORMat {}'.format(mode))

    def set_timebase_x_channel(self, channel):
        """
            Sets the source for single-source immediate measure- ments.
        """
        channel = str(channel)
        if channel in self._available_channels:
            self.device.write("MEASUrement:IMMed:SOUrce1 {}".format(channel))
        else:
            logging.warning("Not supported channel {}, supported are {}".format(channel, self._available_channels))

    def set_timebase_y_channel(self, channel):
        """
            Sets the secondary source for dual-source immediate measurements. For example, power analysis and phase angle measurements.
            NOTE: This command is only available when the Power Analysis Module application key is installed.
        """
        channel = str(channel)
        if channel in self._available_channels:
            self.device.write("MEASUrement:IMMed:SOUrce2 {}".format(channel))
        else:
            logging.warning("Not supported channel {}, supported are {}".format(channel, self._available_channels))
    """
        END ACQUISITION PRIMITIVES
    """



    """
        BEGIN ACQUISITION PRIMITIVES
        Acquisition commands affect the acquisition of waveforms. These commands control mode, averaging, and single-waveform acquisition
    """
    def set_acquisition_mode(self, mode):
        """
        Sets the oscilloscope acquisition mode. This affects all live waveforms
        and is equivalent to setting the Mode option in the Acquire menu.

        Waveforms are the displayed data point values taken from acquisition intervals.
        Each acquisition interval represents a time duration that is determined by the horizontal scale (time per division).

        The oscilloscope sampling system can operate at a rate greater than that indicated by the horizontal scale.
        Therefore, an acquisition interval can include more than one sample.

        The acquisition mode, which you set using this ACQuire:MODe command, determines
        how the final value of the acquisition interval is generated from the many data samples.
        """
        mode = str(mode)
        if mode in self._available_acquisition_modes:
            self.device.write("ACQuire:MODe {}".format(mode))
        else:
            logging.warning("Acquisition mode {} is not supported, supported are {}".format(mode, self._available_acquisition_modes))

    def get_acquisition_mode(self):
        """
            Queries and returns the oscilloscope acquisition mode
        """
        return self.device.write("ACQuire:MODe?")

    def set_average_acquisition_mode_samples_amount(self, amount):
        """
            Sets the number of oscilloscope waveform acquisitions that make up an averaged waveform.
            This command is equivalent to setting the Averages option in the Acquire menu.
        """

        # Check is in 'AVErage' mode
        mode = self.get_acquisition_mode()
        if mode.lower() != "AVErage".lower():
            logging.warning("set_average_acquisition_mode_samples_amount should be called on 'average' acquisition mode but current is '{}'".format(mode))
            return

        if amount in self._available_average_acquisition_mode_samples_amount:
            self.device.write("ACQuire:NUMAVg {}".format(amount))
        else:
            logging.warning("Samples amount {} is not supported, supported are {}".format(amount, self._available_average_acquisition_mode_samples_amount))

    def set_acquisition_memory_depth(self, depth):
        logging.warning("set_acquisition_memory_depth primmitive is not supported, this osciloscope has fixed memory depth of 2.5K")
    """
        END ACQUISITION PRIMITIVES
    """

