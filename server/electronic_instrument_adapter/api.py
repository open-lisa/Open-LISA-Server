import socket
import logging

from .repositories.instruments_repository import InstrumentsRepository
from .protocol.server_protocol import COMMAND_GET_INSTRUMENT, COMMAND_GET_INSTRUMENTS, COMMAND_GET_INSTRUMENT_COMMANDS, COMMAND_SEND_COMMAND, COMMAND_VALIDATE_COMMAND, ServerProtocol


class ElectronicInstrumentAdapter:

    def __init__(self, listening_port):
        self._listening_port = listening_port
        self._instruments_repository = InstrumentsRepository('electronic_instrument_adapter/instrument/instruments.json')

        print("* * * * * * * * * * Instruments List * * * * * * * * * *")
        for instrument in self._instruments_repository.get_all():
            print(instrument)
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")

    def start(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', self._listening_port))
        self._server_socket.listen(0) # Only handles one client

        while True:
            logging.debug("[ElectronicInstrumentAdapter][api][start] - proceed to accept new connection")
            socket_connection, addr = self._server_socket.accept()
            logging.debug('[ElectronicInstrumentAdapter][api][start] - got connection from {}'.format(addr))
            self._server_protocol = ServerProtocol(socket_connection)
            while True:
                try:
                    command = self._server_protocol.get_command()
                    logging.debug("[ElectronicInstrumentAdapter][api][start] - command received: " + command)
                    self._update_instruments_status()
                    if command == COMMAND_GET_INSTRUMENTS:
                        logging.debug("[ElectronicInstrumentAdapter][api][start] - getting instruments")
                        self._server_protocol.handle_get_instruments(self._instruments_repository)
                    elif command == COMMAND_GET_INSTRUMENT:
                        logging.debug("[ElectronicInstrumentAdapter][api][start] - getting specific instrument")
                        self._server_protocol.handle_get_instrument(self._instruments_repository)
                    elif command == COMMAND_GET_INSTRUMENT_COMMANDS:
                        logging.debug("[ElectronicInstrumentAdapter][api][start] - getting instrument commands")
                        self._server_protocol.handle_get_instrument_commands(self._instruments_repository)
                    elif command == COMMAND_VALIDATE_COMMAND:
                        logging.debug("[ElectronicInstrumentAdapter][api][start] - validating instrument command")
                        self._server_protocol.handle_validate_command(self._instruments_repository)
                    elif command == COMMAND_SEND_COMMAND:
                        logging.debug("[ElectronicInstrumentAdapter][api][start] - sending command to instrument")
                        self._server_protocol.handle_send_command(self._instruments_repository)
                    else:
                        logging.error("[ElectronicInstrumentAdapter][api][start] - unknown command '{}'".format(command))
                except ConnectionResetError as ex:
                    logging.info("[ElectronicInstrumentAdapter][api][start] - client socket disconnect {}".format(ex))
                    break
                except Exception as ex:
                    logging.error("[ElectronicInstrumentAdapter][api][start][FATAL_ERROR]: {}".format(ex))
                    break

    def _update_instruments_status(self):
        for instrument in self._instruments_repository.get_all():
            instrument.update_status()