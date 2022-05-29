DEFAULT_BAUDRATE = 921600
DEFAULT_TIMEOUT = None


class RS232Configuration:

    def __init__(self, port, baudrate=DEFAULT_BAUDRATE, timeout=DEFAULT_TIMEOUT):
        self.port = port
        self.baudrate = baudrate if baudrate is not None else DEFAULT_BAUDRATE
        self.timeout = timeout
