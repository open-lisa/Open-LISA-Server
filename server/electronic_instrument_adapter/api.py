import json
import time

from .instrument.constants import INSTRUMENT_STATUS_UNAVAILABLE
from .instrument.errors.command_not_found_error import CommandNotFoundError
from .instrument.errors.invalid_amount_parameters_error import InvalidAmountParametersError
from .instrument.errors.invalid_parameter_error import InvalidParameterError
from .instrument.instrument import Instrument


class ElectronicInstrumentAdapter:

    def __init__(self, listening_port):
        self._listening_port = listening_port
        self._instruments = []

        self.load_instruments()
        print("Instruments List: ******************************")
        for instrument in self._instruments:
            print(instrument)
        print("***************** ******************************")

        # todo: definir nuevo protocolo con socket o USB, no more Flask
        # todo: considerar podder utilizar tanto USB como socket por red LAN, que sea configurable
        # todo: armar un handler de comandos que llame a las funciones de esta api

    def load_instruments(self):
        self._instruments = []
        with open('electronic_instrument_adapter/instrument/instruments.json') as file:
            data = json.load(file)

            for raw_instrument in data:
                instrument = Instrument(
                    raw_instrument["id"],
                    raw_instrument["brand"],
                    raw_instrument["model"],
                    raw_instrument["description"]
                )
                self._instruments.append(instrument)

    def get_instruments(self):
        formatted_instruments = []

        for instrument in self._instruments:
            formatted_instruments.append(instrument.as_dict())

        return json.dumps(formatted_instruments)

    def get_instrument(self, instrument_id):
        for instrument in self._instruments:
            if instrument.id == instrument_id:
                return instrument.as_dict()

        return None

    def get_instrument_commands(self, instrument_id):
        for instrument in self._instruments:
            if instrument.id == instrument_id:
                return json.dumps(instrument.commands_map)

        return None

    # Todo decirle a Ariel que considere este comando para probar validez de comando sin disponibilidad del instrumento
    def validate_command(self, instrument_id, command):
        for instrument in self._instruments:
            if instrument.id == instrument_id:
                try:
                    instrument.validate_command(command)
                except CommandNotFoundError:
                    return "Command not found"
                except InvalidAmountParametersError as e:
                    return "{} Parameters has sent, but {} are required.".format(
                        e.parameters_amount_sent,
                        e.parameters_amount_required
                    )
                except InvalidParameterError as e:
                    return "Parameter in position {} has an invalid format. Correct format is {}, ie: {}.".format(
                        e.position,
                        e.correct_format,
                        e.example
                    )

        return "The command is valid"

    def send_command(self, instrument_id, command):
        for instrument in self._instruments:
            if instrument.id == instrument_id:
                try:
                    if instrument.status == INSTRUMENT_STATUS_UNAVAILABLE:
                        return "Instrument not available."
                    response = instrument.send_command(command)
                    return response
                except CommandNotFoundError:
                    return "Command not found"
                except InvalidAmountParametersError as e:
                    return "{} Parameters has sent, but {} are required.".format(
                        e.parameters_amount_sent,
                        e.parameters_amount_required
                    )
                except InvalidParameterError as e:
                    return "Parameter in position {} has an invalid format. Correct format is {}, ie: {}.".format(
                        e.position,
                        e.correct_format,
                        e.example
                    )

        return None

    def start(self):
        while True:
            # todo: Considerar armar tests para probar estos casos...
            print("Waiting commands ...")
            print("Instruments:")
            print(self.get_instruments())
            print("Instrument example:")
            print(self.get_instrument("USB0::0x0699::0x0363::C107676::INSTR"))
            print("Instrument commands example:")
            print(self.get_instrument_commands("USB0::0x0699::0x0363::C107676::INSTR"))
            print("Instrument validate non-existent command example:")
            print(self.validate_command("USB0::0x0699::0x0363::C107676::INSTR", "pepinardovich"))
            print("Instrument validate existent command example:")
            print(self.validate_command("USB0::0x0699::0x0363::C107676::INSTR", "set_waveform_encoding_ascii"))
            print("Instrument validate existent command with invalid parameters amount example:")
            print(self.validate_command("USB0::0x0699::0x0363::C107676::INSTR", "set_trigger_level 10 20"))
            print("Instrument validate existent command with invalid parameters format example:")
            print(self.validate_command("USB0::0x0699::0x0363::C107676::INSTR", "set_trigger_level ASCII"))
            print("Instrument validate existent command with valid parameter example:")
            print(self.validate_command("USB0::0x0699::0x0363::C107676::INSTR", "set_trigger_level 3.4"))
            time.sleep(10)
