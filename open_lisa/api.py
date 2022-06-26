import serial
import socket
import logging
import traceback
import sys


from .protocol.message_protocol_rs232 import MessageProtocolRS232
from .protocol.message_protocol_tcp import MessageProtocolTCP
from .repositories.instruments_repository import InstrumentsRepository
from .protocol.server_protocol import COMMAND_GET_INSTRUMENT, COMMAND_GET_INSTRUMENTS, COMMAND_GET_INSTRUMENT_COMMANDS, \
    COMMAND_SEND_COMMAND, COMMAND_VALIDATE_COMMAND, COMMAND_DISCONNECT, ServerProtocol

PATH_INSTRUMENTS_REPOSITORY = 'open_lisa/instrument/instruments.json'
MODE_SERIAL = 'SERIAL'
MODE_TCP = 'TCP'
MAX_CONCURRENT_CLIENTS = 1
RS232_EXPECTED_CLIENT_QUESTION = 'OPEN'
RS232_ANSWER_TO_CLIENT_QUESTION = 'LISA'


class OpenLISA:

    def __init__(self, mode, rs232_config, listening_port):
        self._rs232_connection = None
        self._server_protocol = None
        self._mode = mode
        self._rs232_config = rs232_config
        self._listening_port = listening_port
        self._instruments_repository = None

    def start(self):
        while True:
            logging.info("Waiting for client connection...")
            if self._mode == MODE_SERIAL:
                self._server_protocol = self._rs232_wait_connection()
            elif self._mode == MODE_TCP:
                self._server_protocol = self._tcp_wait_connection()
            else:
                logging.error("OpenLisa started with invalid mode: {}".format(self._mode))
                exit(1)

            self._instruments_repository = InstrumentsRepository(PATH_INSTRUMENTS_REPOSITORY)
            self._list_instruments()

            while True:
                try:
                    command = self._server_protocol.get_command()
                    logging.info("[OpenLISA][api][start] - command received: " + command)
                    self._update_instruments_status()
                    if command == COMMAND_GET_INSTRUMENTS:
                        logging.debug("[OpenLISA][api][start] - getting instruments")
                        self._server_protocol.handle_get_instruments(self._instruments_repository)
                    elif command == COMMAND_GET_INSTRUMENT:
                        logging.debug("[OpenLISA][api][start] - getting specific instrument")
                        self._server_protocol.handle_get_instrument(self._instruments_repository)
                    elif command == COMMAND_GET_INSTRUMENT_COMMANDS:
                        logging.debug("[OpenLISA][api][start] - getting instrument commands")
                        self._server_protocol.handle_get_instrument_commands(self._instruments_repository)
                    elif command == COMMAND_VALIDATE_COMMAND:
                        logging.debug("[OpenLISA][api][start] - validating instrument command")
                        self._server_protocol.handle_validate_command(self._instruments_repository)
                    elif command == COMMAND_SEND_COMMAND:
                        logging.debug("[OpenLISA][api][start] - sending command to instrument")
                        self._server_protocol.handle_send_command(self._instruments_repository)
                    elif command == COMMAND_DISCONNECT:
                        logging.info("[OpenLISA][api][start] - client order disconnect")
                        # self._server_protocol.handle_disconnect_command()
                        break
                    else:
                        logging.error(
                            "[OpenLISA][api][start] - unknown command '{}'".format(command))
                except ConnectionResetError as ex:
                    logging.info("[OpenLISA][api][start] - client socket disconnect {}".format(ex))
                    break
                except Exception as ex:
                    logging.error("[OpenLISA][api][start][FATAL_ERROR]: {}".format(ex))
                    traceback.print_exc()
                    break

    def _update_instruments_status(self):
        for instrument in self._instruments_repository.get_all():
            instrument.update_status()

    def _list_instruments(self):
        logging.debug("* * * * * * * * * * Instruments List * * * * * * * * * *")
        for instrument in self._instruments_repository.get_all():
            logging.debug(instrument)
        logging.debug("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")

    def _rs232_wait_connection(self):
        if not self._rs232_connection:
            self._rs232_create_connection()

        while True:
            logging.info("Waiting for RS232 client question...")
            client_question = self._rs232_connection.read(4)
            logging.info("Question received from client: {}".format(client_question.decode()))
            if RS232_EXPECTED_CLIENT_QUESTION == client_question.decode():
                logging.info("Question match with expected. Starting RS232 connection...")
                self._rs232_connection.write(RS232_ANSWER_TO_CLIENT_QUESTION.encode('utf-8'))
                break
            else:
                logging.info("Question does not match the expected, still waiting for a client...")

        return ServerProtocol(MessageProtocolRS232(self._rs232_connection))

    def _rs232_create_connection(self):
        try:
            self._rs232_connection = serial.Serial(
                port=self._rs232_config.port,
                baudrate=self._rs232_config.baudrate,
                timeout=self._rs232_config.timeout)

            logging.info("Serial RS232 connection created at {} with baudrate of {}".format(
                self._rs232_config.port,
                self._rs232_config.baudrate
            ))

        except serial.SerialException:
            logging.error("Error on open serial connection on {}".format(self._rs232_config.port))
            traceback.print_exception(*sys.exc_info())
            exit(1)

        if not self._rs232_connection.is_open:
            self._rs232_connection.open()

    def _tcp_wait_connection(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', self._listening_port))
        server_socket.listen(MAX_CONCURRENT_CLIENTS - 1)  # Only handles one client

        logging.debug("[OpenLISA][api][start] - TPC proceed to accept new connection")
        socket_connection, addr = server_socket.accept()
        logging.debug('[OpenLISA][api][start] - TCP got connection from {}'.format(addr))

        return ServerProtocol(MessageProtocolTCP(socket_connection))
