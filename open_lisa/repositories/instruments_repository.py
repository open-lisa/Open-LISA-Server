import json
import logging
import os
import pyvisa
from open_lisa.domain.instrument.instrument import Instrument
from open_lisa.exceptions.instrument_creation_error import InstrumentCreationError
from open_lisa.exceptions.instrument_deletion_error import InstrumentDeletionError
from open_lisa.exceptions.instrument_not_found import InstrumentNotFoundError
from open_lisa.exceptions.instrument_update_error import InstrumentUpdateError
from open_lisa.repositories.commands_repository import CommandsRepository
from open_lisa.repositories.json_repository import JSONRepository


class InstrumentRepository(JSONRepository):
    def __init__(self, path=os.getenv("DATABASE_INSTRUMENTS_PATH")) -> None:
        path = os.getenv("DATABASE_INSTRUMENTS_PATH") if not path else path
        super().__init__(path)
        self._commands_repository = CommandsRepository()

    def get_all(self):
        instruments = []
        instrument_dicts = super().get_all()
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        for instrument_dict in instrument_dicts:
            physical_address = instrument_dict["physical_address"]
            pyvisa_resource = None
            instrument_id = instrument_dict["id"]

            if physical_address in resources:
                try:
                    pyvisa_resource = rm.open_resource(physical_address)
                except pyvisa.errors.VisaIOError as ex:
                    # Registered instruments should never be detected as BUSY
                    logging.error(
                        "[OpenLISA][InstrumentRepository][get_all] Error opening pyvisa resource: {} for instrument {}".format(ex, instrument_dict))

            instrument_commands = self._commands_repository.get_instrument_commands(
                instrument_id=instrument_id, pyvisa_resource=pyvisa_resource)
            instrument = Instrument.from_dict(
                dict=instrument_dict,
                commands=instrument_commands,
                pyvisa_resource=pyvisa_resource
            )
            instruments.append(instrument)

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

    def get_by_id(self, id) -> Instrument:
        id = int(id)
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

    def create_instrument(self, new_instrument) -> Instrument:
        try:
            new_id = self.add(new_instrument)
        except Exception:
            raise InstrumentCreationError(
                "could not create instrument {}".format(new_instrument))
        return self.get_by_id(new_id)

    def update_instrument(self, id, updated_instrument) -> Instrument:
        id = int(id)
        instrument = self.get_by_id(id)
        valid_keys = list(instrument.to_dict().keys())

        payload_keys = list(updated_instrument.keys())
        invalid_payload_keys = [k for k in payload_keys if k not in valid_keys]
        if len(invalid_payload_keys) > 0:
            raise InstrumentUpdateError(
                "keys {} are invalid for instrument update".format(invalid_payload_keys))

        self.update_by_id(id, updated_instrument)
        return self.get_by_id(id)

    def delete_instrument(self, id) -> Instrument:
        id = int(id)
        instrument = self.get_by_id(id)
        try:
            self.remove_by_id(id)
        except Exception as e:
            raise InstrumentDeletionError(
                "could not delete instrument: {}".format(str(e)))
        return instrument
