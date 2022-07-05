from enum import Enum

from open_lisa.domain.instrument.constants import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE
from open_lisa.exceptions.command_not_found_error import CommandNotFoundError
from open_lisa.exceptions.instrument_unavailable_error import InstrumentUnavailableError


class InstrumentType(Enum):
    SCPI = "scpi"
    CLIB = "clib"

    @staticmethod
    def from_str(string_type):
        if string_type == str(InstrumentType.CLIB):
            return InstrumentType.CLIB
        elif string_type == str(InstrumentType.SCPI):
            return InstrumentType.SCPI

    def __str__(self):
        return self.name


# TODO: change name to Instrument when all is integrated and legacy code removed
class Instrument:
    def __init__(self, id, physical_address, brand, model, type, description="",
                 commands=[], pyvisa_resource=None):
        assert isinstance(type, InstrumentType)
        self.id = id
        self.physical_address = physical_address
        self.brand = brand
        self.model = model
        self.type = type
        self.description = description
        self.pyvisa_resource = pyvisa_resource
        self._commands = commands

        if pyvisa_resource:
            # If pyvisa_resource was provided the SCPI commands
            # are ready to be executed, so the instrument is in AVAILABLE status
            self.status = INSTRUMENT_STATUS_AVAILABLE
        elif type == InstrumentType.CLIB:
            # TODO: if CLIB instruments are detected with pyvisa we can add
            # physical_address to them and set instrument status correctly
            self.status = INSTRUMENT_STATUS_AVAILABLE
        else:
            # Instrument is SCPI type and no pyvisa resource was provided
            self.status = INSTRUMENT_STATUS_UNAVAILABLE

    @staticmethod
    def from_dict(dict, commands, pyvisa_resource):
        return Instrument(
            id=dict["id"],
            physical_address=dict["physical_address"],
            brand=dict["brand"],
            model=dict["model"],
            type=InstrumentType.from_str(dict["type"]),
            description=dict["description"],
            commands=commands,
            pyvisa_resource=pyvisa_resource,
        )

    @property
    def commands_map(self):
        commands_map = {}
        for command in self._commands:
            commands_map[command.name] = command.to_dict(instrument_id=self.id)
        return commands_map

    def to_dict(self):
        return {
            "id": self.id,
            "physical_address": self.physical_address,
            "brand": self.brand,
            "model": self.model,
            "description": self.description,
            "status": self.status,
        }

    def __str__(self):
        return self.to_dict()

    def send_command(self, command_name, command_parameters_values=[]):
        if not self.status == INSTRUMENT_STATUS_AVAILABLE:
            raise InstrumentUnavailableError(
                "instrument {} {} not available for sending command".format(self.brand, self.model))
        command = self.__get_command_by_name(command_name)
        return command.execute(command_parameters_values)

    def validate_command(self, command_name, command_parameters_values=[]):
        command = self.__get_command_by_name(command_name=command_name)

        if len(command_parameters_values):
            command.parameters.validate_parameters_values(
                command_parameters_values)

    def __get_command_by_name(self, command_name):
        for command in self._commands:
            if command.name == command_name:
                return command
        raise CommandNotFoundError("command {} not registered in instrument {} {}".format(
            command_name, self.brand, self.model))
