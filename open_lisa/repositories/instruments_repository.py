import json
import logging
import os
import pyvisa
from open_lisa.domain.instrument.instrument import InstrumentType, InstrumentV2
from open_lisa.instrument.instrument import Instrument
from open_lisa.exceptions.instrument_not_found import InstrumentNotFoundError
from open_lisa.repositories.commands_repository import CommandsRepository
from open_lisa.repositories.json_repository import JSONRepository

DEFAULT_PATH = os.getenv("DATABASE_INSTRUMENTS_PATH")


class InstrumentRepositoryV2(JSONRepository):
    def __init__(self, path=DEFAULT_PATH) -> None:
        super().__init__(path)
        self._commands_repository = CommandsRepository()

    def get_all(self):
        instruments = []
        instrument_dicts = super().get_all()
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        for instrument_dict in instrument_dicts:
            physical_address = instrument_dict["physical_address"]

            if physical_address in resources:
                try:
                    pyvisa_resource = None
                    instrument_id = instrument_dict["id"]
                    instrument_type = InstrumentType.from_str(
                        instrument_dict["type"])
                    if InstrumentType.SCPI == instrument_type:
                        pyvisa_resource = rm.open_resource(physical_address)

                    instrument = InstrumentV2(
                        id=instrument_id,
                        physical_address=physical_address,
                        brand=instrument_dict["brand"],
                        model=instrument_dict["model"],
                        type=instrument_type,
                        description=instrument_dict["description"],
                        commands=self._commands_repository.get_instrument_commands(
                            instrument_id=instrument_id, pyvisa_resource=pyvisa_resource),
                        pyvisa_resource=pyvisa_resource,
                    )
                    instruments.append(instrument)
                except pyvisa.errors.VisaIOError as ex:
                    # Registered instruments should never be detected as BUSY
                    logging.error(
                        "[OpenLISA][InstrumentRepository][get_all] Error opening pyvisa resource: {} for instrument {}".format(ex, instrument_dict))

        return instruments

    def get_all_as_json(self):
        instruments = self.get_all()
        formatted_instruments = []

        for instrument in instruments:
            formatted_instruments.append(instrument.to_dict())

        return json.dumps(formatted_instruments)

    def get_by_physical_address(self, physical_addres):
        instruments = self.get_all()
        match = None
        for ins in instruments:
            if ins.physical_address == physical_addres:
                match = ins
                break

        if not match:
            raise InstrumentNotFoundError(
                "instrument not found for physical address {}".format(physical_addres))

        return match

    def get_by_id(self, id):
        instruments = self.get_all()
        match = None
        for ins in instruments:
            if ins.id == id:
                match = ins
                break

        if not match:
            raise InstrumentNotFoundError(
                "instrument not found for id {}".format(id))

        return match


class InstrumentsRepository:
    def __init__(self, path) -> None:
        self._instruments = []

        # Registered instruments
        with open(path) as file:
            data = json.load(file)

            for raw_instrument in data:
                instrument = Instrument(
                    raw_instrument["id"],
                    raw_instrument["brand"],
                    raw_instrument["model"],
                    raw_instrument["description"],
                    raw_instrument["command_file"]
                )
                self._instruments.append(instrument)

        # Not registered instruments
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        for resource_id in resources:
            try:
                self.find_one(resource_id)
            except InstrumentNotFoundError:
                instrument = Instrument(
                    id=resource_id,
                    brand="UNKNOWN",
                    model="UNKNOWN",
                    description="Not registered instrument",
                    command_file=None
                )
                self._instruments.append(instrument)

    def get_all(self):
        return self._instruments

    def get_all_as_json(self):
        formatted_instruments = []

        for instrument in self._instruments:
            formatted_instruments.append(instrument.as_dict())

        return json.dumps(formatted_instruments)

    def find_one(self, id):
        match = None
        for ins in self._instruments:
            if ins.id == id:
                match = ins
                break

        if not match:
            raise InstrumentNotFoundError("instrument {} not found".format(id))

        return match
