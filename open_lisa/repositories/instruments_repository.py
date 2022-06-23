import json
import logging
from open_lisa.instrument.constants import INSTRUMENT_STATUS_AVAILABLE, INSTRUMENT_STATUS_UNAVAILABLE
import pyvisa
from open_lisa.instrument.instrument import Instrument, InstrumentV2
from open_lisa.exceptions.instrument_not_found import InstrumentNotFoundError
from open_lisa.repositories.json_repository import JSONRepository

DEFAULT_PATH = 'data/database/instruments.db.json'


class InstrumentRepositoryV2(JSONRepository):
    def __init__(self, path=DEFAULT_PATH) -> None:
        super().__init__(path)

    def get_all():
        instruments = []
        instrument_dicts = super().get_all()
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        for inststrument_dict in instrument_dicts:
            physical_address = inststrument_dict["physical_address"]

            if resources.__contains__(physical_address):
                try:
                    pyvisa_resource = rm.open_resource(physical_address)
                    instrument = InstrumentV2(
                        id=inststrument_dict["id"],
                        physical_address=physical_address,
                        brand=inststrument_dict["brand"],
                        model=inststrument_dict["model"],
                        description=inststrument_dict["description"],
                        pyvisa_resource=pyvisa_resource,
                        status=INSTRUMENT_STATUS_AVAILABLE
                    )
                    instruments.append(instrument)
                except pyvisa.errors.VisaIOError as ex:
                    # NOTE: no creo que tenga sentido crear instrumentos en estado busy
                    logging.debug(
                        "[OpenLISA][InstrumentRepository][get_all] Error opening pyvisa resource: {}".format(ex))
            else:
                instrument = InstrumentV2(
                    id=inststrument_dict["id"],
                    physical_address=physical_address,
                    brand=inststrument_dict["brand"],
                    model=inststrument_dict["model"],
                    description=inststrument_dict["description"],
                    pyvisa_resource=None,

                    # TODO: be better than this
                    status=INSTRUMENT_STATUS_AVAILABLE if "MOCK_INSTRUMENT" in inststrument_dict[
                        "brand"] else INSTRUMENT_STATUS_UNAVAILABLE,
                )
                # TODO: no sabemos cómo determinar el status de instrumentos
                # que no se conectan por por pyvisa (el unico instrument con CLib siempre
                # lo poniamos en AVAILABLE por ser el mock :thinking:)
                instruments.append(instrument)

        # TODO: no sé si tiene sentido crear instrumentos en estado NOT_REGISTERED
        # o BUSSY ya que son simplemente direcciones fisicas por el momento o recursos
        # pyvisa... de hecho en la UI vamos a mostrar (o queremos mostrar) las direcciones
        # fisicas detectadas a las que no se tiene asociado un instrumento

        # NOTE: notar que el "status" del instrumento es actualizado en cada llamada a
        # get_all() del repositorio, con este enfoque la clase InstrumentV2 no tiene que
        # saber como lidiar con el pyvisa_resource, es simplemente una dependencia de
        # instanciación. Me parece que tiene sentido que esté acá ya que los pyvisa.resources
        # son justamente una fuente de datos como lo es el JSON file
        return instruments

    def get_all_as_json(self):
        instruments = self.get_all()
        formatted_instruments = []

        for instrument in instruments:
            formatted_instruments.append(instrument.to_dict())

        return json.dumps(formatted_instruments)

    # TODO: we should use instrument_id from sdk and UI in order to identify instruments
    def get_by_physical_address(self, physical_addres):
        instruments = self.get_all()
        match = None
        for ins in instruments:
            if ins.physical_address == physical_addres:
                match = ins
                break

        if not match:
            raise InstrumentNotFoundError(
                "instrument {} not found".format(physical_addres))

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
