import json
import logging
import os
import pyvisa
from open_lisa.domain.instrument.instrument import Instrument
from open_lisa.exceptions.base_exception import OpenLISAException
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
                except Exception as ex:
                    logging.error(
                        "[OpenLISA][InstrumentRepository][get_all] Error opening pyvisa resource: {} for instrument {}".format(ex, instrument_dict))
                    raise OpenLISAException(
                        "could not open pyvisa resource: {}".format(physical_address))

            instrument_commands = self._commands_repository.get_instrument_commands(
                instrument_id=instrument_id, pyvisa_resource=pyvisa_resource)
            instrument = Instrument.from_dict(
                dict=instrument_dict,
                commands=instrument_commands,
                pyvisa_resource=pyvisa_resource
            )
            instruments.append(instrument)

        return instruments

    def get_pyvisa_available_physical_addresses(self):
        instrument_dicts = super().get_all()

        # Gets only the physical addresses of the registered instruments
        registered_physical_addresses = map(
            lambda instrument: instrument["physical_address"], instrument_dicts)
        rm = pyvisa.ResourceManager()

        # fetch physical addresses and ResourceInfo from pyvisa
        # -> Dict[str, ResourceInfo]
        pyvisa_resources_with_info = rm.list_resources_info()
        pyvisa_physical_addresses = pyvisa_resources_with_info.keys()

        not_registered_physical_addresses = filter(
            lambda physical_address: physical_address not in registered_physical_addresses, pyvisa_physical_addresses
        )
        return list(map(lambda not_registered_physical_address: {
            # NOTE: Here could be added more information that is provided by pyvisa
            # check the docs https://pyvisa.readthedocs.io/en/latest/api/resourcemanager.html#pyvisa.highlevel.ResourceInfo
            "physical_address": not_registered_physical_address,
            "interface_type": str(pyvisa_resources_with_info[not_registered_physical_address].interface_type),
            "interface_board_number": str(pyvisa_resources_with_info[not_registered_physical_address].interface_board_number),
            "resource_class": str(pyvisa_resources_with_info[not_registered_physical_address].resource_class),
            "resource_name": str(pyvisa_resources_with_info[not_registered_physical_address].resource_name),
            "alias": str(pyvisa_resources_with_info[not_registered_physical_address].alias)
        }, not_registered_physical_addresses))

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
        id = str(id)
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
        new_id = None
        try:
            new_id = self.add(new_instrument)
            return self.get_by_id(new_id)
        except Exception:
            if new_id:
                self.delete_instrument(id=new_id)
            raise InstrumentCreationError(
                "could not create instrument {}".format(new_instrument))

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
            # Delete all instrument commands
            commands_dicts = self._commands_repository.get_by_key_value(
                key="instrument_id", value=id)
            for command_dict in commands_dicts:
                self._commands_repository.delete_command(command_dict['id'])
        except Exception as e:
            raise InstrumentDeletionError(
                "could not delete instrument: {}".format(str(e)))
        return instrument
