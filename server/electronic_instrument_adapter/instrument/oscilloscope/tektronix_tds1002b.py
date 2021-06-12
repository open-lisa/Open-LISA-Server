import json
import logging
from .oscilloscope import Oscilloscope


class Tektronix_TDS1002B(Oscilloscope):
    def __init__(self, id):
        with open('electronic_instrument_adapter/instrument/oscilloscope/configs/oscilloscope_tektronix_tds1002b.json') as file:
            cfg = json.load(file)
            self._available_channels = [channel["value"] for channel in cfg["channels"]["amount"]]
            self._available_channel_attenuations_factors = [attenuation["value"] for attenuation in cfg["channels"]["attenuation_factors"]]
            self._available_timebase_modes = [mode["value"] for mode in cfg["timebase"]["modes"]]
            self._available_acquisition_modes = [mode["value"] for mode in cfg["acquisition"]["modes"]]
            self._available_average_acquisition_mode_samples_amount =[amount["value"] for amount in cfg["acquisition"]["average_mode_samples_amount"]]
            self._available_trigger_modes = [mode["value"] for mode in cfg["trigger"]["modes"]]
            self._available_trigger_types = [type["value"] for type in cfg["trigger"]["types"]]
            self._available_trigger_edge_types = [type["value"] for type in cfg["trigger"]["edge_types"]]
            self._available_trigger_edge_sources = [source["value"] for source in cfg["trigger"]["edge_sources"]]
            self._available_waveform_encodings = [encoding["value"] for encoding in cfg["waveform"]["encodings"]]
            self._available_waveform_endianness = [endian["value"] for endian in cfg["waveform"]["endianness"]]
            self._available_waveform_sources = [src["value"] for src in cfg["waveform"]["sources"]]
            self._available_waveform_points_formats = [fmt["value"] for fmt in cfg["waveform"]["points_formats"]]

        super().__init__(id, "Tektronix", "TDS1002B")

    def set_initial_configuration(self):
        self.configuration.volts_scale = 5.0
        self.configuration.time_scale = 0.000500

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

        command = str("{}:VOLts {}".format(channel, volts_scale))
        self.device.write(command)

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

        command = str("{}:PRObe {}".format(channel, probe))
        self.device.write(command)
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
        command = str("HORizontal:MAIn:SCAle {}".format(seconds))
        self.device.write(command)

    def set_timebase_mode(self, mode):
        """
            Sets the oscilloscope display format.
        """
        mode = str(mode)
        if mode in self._available_timebase_modes:
            command = str("DISplay:FORMat {}".format(mode))
            self.device.write(command)

    def set_timebase_x_channel(self, channel):
        """
            Sets the source for single-source immediate measure- ments.
        """
        channel = str(channel)
        if channel in self._available_channels:
            command = str("MEASUrement:IMMed:SOUrce1 {}".format(channel))
            self.device.write(command)
        else:
            logging.warning("Not supported channel {}, supported are {}".format(channel, self._available_channels))

    def set_timebase_y_channel(self, channel):
        """
            Sets the secondary source for dual-source immediate measurements. For example, power analysis and phase angle measurements.
            NOTE: This command is only available when the Power Analysis Module application key is installed.
        """
        channel = str(channel)
        if channel in self._available_channels:
            command = str("MEASUrement:IMMed:SOUrce2 {}".format(channel))
            self.device.write(command)
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
            command = str("ACQuire:MODe {}".format(mode))
            self.device.write(command)
        else:
            logging.warning("Acquisition mode {} is not supported, supported are {}".format(mode, self._available_acquisition_modes))

    def get_acquisition_mode(self):
        """
            Queries and returns the oscilloscope acquisition mode
        """
        return self.device.query("ACQuire:MODe?")

    def set_average_acquisition_mode_samples_amount(self, amount):
        """
            Sets the number of oscilloscope waveform acquisitions that make up an averaged waveform.
            This command is equivalent to setting the Averages option in the Acquire menu.
        """

        # Check is in 'AVErage' mode
        mode = self.get_acquisition_mode()
        if mode.lower() != "AVErage".lower():
            logging.warning("set_average_acquisition_mode_samples_amount should be called on 'average' acquisition mode but current is '{}'".format(mode))
            return

        if amount in self._available_average_acquisition_mode_samples_amount:
            command = str("ACQuire:NUMAVg {}".format(amount))
            self.device.write(command)
        else:
            logging.warning("Samples amount {} is not supported, supported are {}".format(amount, self._available_average_acquisition_mode_samples_amount))

    def set_acquisition_memory_depth(self, depth):
        logging.warning("set_acquisition_memory_depth primmitive is not supported, this osciloscope has fixed memory depth of 2.5K")
    """
        END ACQUISITION PRIMITIVES
    """



    """
        BEGIN TRIGGER PRIMITIVES
        Trigger commands control all aspects of oscilloscope triggering.

        The three types of triggers are edge, pulse width, and video.
        Edge triggering is the default type. Edge triggering lets you acquire a waveform
        when the signal passes through a voltage level of your choosing.
        Pulse width triggering lets you trigger on normal or aberrant pulses.
        Video triggering adds the capability of triggering on video fields and lines.
    """
    def force_trigger(self):
        """
            FORCe creates a trigger event. If TRIGger:STATE is REAdy,
            the acquisition will complete; otherwise this command will be ignored.
            This is equivalent to selecting FORCE TRIG on the front panel.
        """
        self.device.write("TRIGger FORCe")

    def set_trigger_mode(self, mode):
        """
            Sets the trigger mode for the Edge and Pulse widths trigger types.
        """
        mode = str(mode)
        if mode in self._available_trigger_modes:
            command = str("TRIGger:MAIn:MODe {}".format(mode))
            self.device.write(command)
        else:
            logging.warning("Trigger mode {} is not supported, supported are {}".format(mode, self._available_trigger_modes))

    def set_trigger_type(self, type):
        """
            Sets the type of oscilloscope trigger. This is equivalent to setting the Type option in the Trigger menu.
        """
        type = str(type)
        if type in self._available_trigger_types:
            command = str("TRIGger:MAIn:TYPe {}".format(type))
            self.device.write(command)
        else:
            logging.warning("Trigger type {} is not supported, supported are {}".format(type, self._available_trigger_types))

    def get_trigger_type(self):
        """
            Queries and returns the type of oscilloscope trigger.
        """
        return self.device.query("TRIGger:MAIn:TYPe?")

    def set_trigger_edge_type(self, type):
        """
            Selects a rising or falling slope for the edge trigger. This is equivalent to setting the Slope option in the Trigger menu.
        """
        type = str(type)
        trigger_type = self.get_trigger_type()
        if trigger_type != "EDGE":
            logging.warning("Trigger type must be EDGE to set the edge type, current trigger type is {}".format(trigger_type))
            return

        if type in self._available_trigger_edge_types:
            command = str("TRIGger:MAIn:EDGE:SLOpe {}".format(type))
            self.device.write(command)
        else:
            logging.warning("Trigger edge type {} is not supported, supported are {}".format(type, self._available_trigger_edge_types))

    def set_trigger_edge_source(self, src):
        """
            Selects a rising or falling slope for the edge trigger.
            This is equivalent to setting the Slope option in the Trigger menu.
        """
        src = str(src)
        trigger_type = self.get_trigger_type()
        if trigger_type != "EDGE":
            logging.warning("Trigger type must be EDGE to set the edge source, current trigger type is {}".format(trigger_type))
            return

        if src in self._available_trigger_edge_sources:
            command = str("TRIGger:MAIn:EDGE:SOUrce {}".format(src))
            self.device.write(command)
        else:
            logging.warning("Trigger edge source {} is not supported, supported are {}".format(src, self._available_trigger_edge_sources))

    def set_trigger_level(self, level):
        """
            Sets the oscilloscope edge and pulse width trigger level in volts.
            This command is equivalent to adjusting the front-panel TRIGGER LEVEL knob.

            NOTE. When the edge trigger source is set to AC LINE,
            the oscilloscope ignores the set form of the command and generates event 221 (Settings conflict).
            When the edge trigger source is set to AC LINE, the query form of the command returns zero.
        """
        try:
            float(level)
        except ValueError:
            logging.error("Trigger level '{}' could not be parsed as float number".format(level))
            return

        level = str(level)
        trigger_type = self.get_trigger_type()
        if trigger_type != "EDGE" and trigger_type != "PULse":
            logging.warning("Trigger type must be EDGE or PULse to set trigger level, current trigger type is {}".format(trigger_type))
            return

        command = str("TRIGger:MAIn:LEVel {}".format(level))
        self.device.write(command)
    """
        END TRIGGER PRIMITIVES
    """



    """
        BEGIN WAVEFORM PRIMITIVES
    """
    def set_waveform_encoding(self, encoding):
        """
            Sets the format of the waveform data. This command is equivalent to
            setting WFMPre:ENCdg, WFMPre:BN_Fmt, and WFMPre:BYT_Or as shown in Table 2-29 on page 2-88.
            Setting the DATa:ENCdg value causes the corresponding WFMPre values to update.
            Setting the WFMPre value causes the corresponding DATa:ENCdg values to update.
        """
        encoding = str(encoding)
        if encoding in self._available_waveform_encodings:
            command = str("DATa:ENCdg {}".format(encoding))
            self.device.write(command)
        else:
            logging.warning("Waveform encoding '{}' is not supported, supported are {}".format(encoding, self._available_waveform_encodings))

    def get_waveform_encoding(self):
        """
            Queries the format of the waveform data.
        """
        return self.device.query("DATa:ENCdg?")

    def set_waveform_endianness(self, endianness):
        """
            Sets the waveform endianness to the specified
        """
        endianness = str(endianness)
        if endianness not in self._available_waveform_endianness:
            logging.warning("Waveform endianness '{}' is not supported, supported are {}".format(endianness, self._available_waveform_endianness))
            return

        encoding = self.get_waveform_encoding()
        if encoding not in ["RIBinary", "RPBinary", "SRIbinary", "SRPbinary"]:
            logging.warning("Waveform endianness does not apply for ASCII encoding")
            return

        if endianness == "LITTLEENDIAN":
            if encoding == "RIBinary":
                command = str("DATa:ENCdg SRIbinary")
            elif encoding == "RPBinary":
                command = str("DATa:ENCdg SRPbinary")
            else:
                logging.info("Waveform endianness is already LITTLEENDIAN")
                return
        elif endianness == "BIGENDIAN":
            if encoding == "SRIbinary":
                command = str("DATa:ENCdg RIBinary")
            elif encoding == "SRPbinary":
                command = str("DATa:ENCdg RPBinary")
            else:
                logging.info("Waveform endianness is already BIGENDIAN")
                return

        self.device.write(command)

    def set_waveform_source(self, src):
        """
            Sets or queries which waveform will be transferred from the oscilloscope
            by the CURVe?, WFMPre?, or WAVFrm? queries. You can transfer only one waveform at a time.
        """
        src = str(src)
        if src not in self._available_waveform_sources: # TODO: Check if supports more than REFA and REFB memory storage locations
            logging.warning("Waveform source '{}' is not supported, supported are {}".format(src, self._available_waveform_sources))
            return

        command = str("DATa:SOUrce {}".format(src))
        self.device.write(command)

    def set_waveform_points_format(self, fmt):
        """
            The set form of this command sets the format (Y or ENV) of the reference
            waveform specified by the DATa:DESTination command.

            The query form returns the format of the waveform specified by the
            DATa:SOUrce command, if that waveform is on or displayed.
            If the waveform is not displayed, the query form of this command
            generates an error and returns event code 2244.
        """
        fmt = str(fmt)
        if fmt not in self._available_waveform_sources: # TODO: Validar con Cristhian si equivale a mode = RAW
            logging.warning("Waveform point format '{}' is not supported, supported are {}".format(fmt, self._available_waveform_points_formats))
            return

        command = str("WFMPre:PT_Fmt {}".format(fmt))
        self.device.write(command)
    """
        END WAVEFORM PRIMITIVES
    """


