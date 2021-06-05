import requests
from ..domain.exceptions.sdk_exception import ElectronicInstrumentAdapterException
from ..domain.exceptions.could_not_connect_to_server import CouldNotConnectToServerException
from ..domain.instruments.instrument import Instrument
from ..logging import log

class ApiClient:
  def __init__(self, host, port, timeout=5):
    try:
      self._h = host
      self._p = port
      self._base_url = "{}:{}".format(host, port)
      self._tout = timeout

      # Check server is running
      ping_url = "{}/ping".format(self._base_url)
      log.debug("Hitting {}".format(ping_url))
      r = requests.get(ping_url, timeout=self._tout)
      log.debug("Ping status code {}".format(r.status_code))

      if r.status_code != requests.codes.ok:
        raise CouldNotConnectToServerException("could not connect with server at {}".format(self._base_url))
    except Exception as e:
      log.error(e)
      raise CouldNotConnectToServerException("could not connect with server at {}".format(self._base_url))


  def get_connected_instruments(self):
    url = '{}/instrument'.format(self._base_url)
    log.debug("Hitting {}".format(url))
    r = requests.get(url=url, timeout=self._tout)

    if r.status_code == requests.codes.ok:
      return [Instrument.from_dict(d) for d in r.json()]
    else:
      raise ElectronicInstrumentAdapterException("could not get connected instruments from server: {}".format(r.text))