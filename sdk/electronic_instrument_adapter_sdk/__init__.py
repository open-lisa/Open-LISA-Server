from .domain.exceptions.instrument_not_found import InstrumentNotFoundException
from .logging import log
from .api_client.api_client import ApiClient


class EIA:
    def __init__(self, host, port):
        log.info("Initializating SDK")
        self._client = ApiClient(host, port)

    def disconnect(self):
        self._client.disconnect()

    def list_instruments(self):
        """
    Returns the list of Instrument objects that are connected and identified by the server
    """
        return self._client.get_instruments()

    def get_instrument(self, id):
        """
    Returns a Instrument object that are connected and identified by the server
    """
        instruments = self.list_instruments()
        for i in instruments:
            if i.ID == id:
                return i

        raise InstrumentNotFoundException
