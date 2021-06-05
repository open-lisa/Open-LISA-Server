from .logging import log
from .api_client.api_client import ApiClient

class EIA:
  def __init__(self, host, port):
    log.info("Initializating SDK")
    self._client = ApiClient(host, port)

  def list_instruments(self):
    """
    Returns the list of Instrument objects that are connected and identified by the server
    """
    return self._client.get_connected_instruments()


