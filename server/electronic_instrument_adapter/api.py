import time

import serial
import socket
import logging
import traceback
import sys


from .protocol.message_protocol_rs232 import MessageProtocolRS232
from .protocol.message_protocol_tcp import MessageProtocolTCP
from .repositories.instruments_repository import InstrumentsRepository
from .protocol.server_protocol import COMMAND_GET_INSTRUMENT, COMMAND_GET_INSTRUMENTS, COMMAND_GET_INSTRUMENT_COMMANDS, \
    COMMAND_SEND_COMMAND, COMMAND_VALIDATE_COMMAND, ServerProtocol

PATH_INSTRUMENTS_REPOSITORY = 'electronic_instrument_adapter/instrument/instruments.json'
MODE_SERIAL = 'SERIAL'
MODE_TCP = 'TCP'
MAX_CONCURRENT_CLIENTS = 1
RS232_EXPECTED_CLIENT_QUESTION = 'OPEN'
RS232_ANSWER_TO_CLIENT_QUESTION = 'LISA'


class ElectronicInstrumentAdapter:

    def __init__(self, mode, rs232_config, listening_port):
        self._server_protocol = None
        self._mode = mode
        self._rs232_config = rs232_config
        self._listening_port = listening_port
        self._instruments_repository = None

    def start(self):
        if self._mode == MODE_SERIAL:
            self._server_protocol = self._rs232_wait_connection()
        elif self._mode == MODE_TCP:
            self._server_protocol = self._tcp_wait_connection()
        else:
            logging.error("OpenLisa started with invalid mode: {}".format(self._mode))
            exit(1)

        self._instruments_repository = InstrumentsRepository(PATH_INSTRUMENTS_REPOSITORY)
        self._list_instruments()

        logging.info("Waiting for commands from client")
        while True:
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
                        logging.error(
                            "[ElectronicInstrumentAdapter][api][start] - unknown command '{}'".format(command))
                except ConnectionResetError as ex:
                    logging.info("[ElectronicInstrumentAdapter][api][start] - client socket disconnect {}".format(ex))
                    break
                except Exception as ex:
                    logging.error("[ElectronicInstrumentAdapter][api][start][FATAL_ERROR]: {}".format(ex))
                    traceback.print_exc()
                    break

    def _update_instruments_status(self):
        for instrument in self._instruments_repository.get_all():
            instrument.update_status()

    def _list_instruments(self):
        print("* * * * * * * * * * Instruments List * * * * * * * * * *")
        for instrument in self._instruments_repository.get_all():
            print(instrument)
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * *")

    def _rs232_wait_connection(self):
        rs232_connection = None
        try:
            rs232_connection = serial.Serial(
                port=self._rs232_config.port,
                baudrate=self._rs232_config.baudrate,
                timeout=self._rs232_config.timeout)
        except serial.SerialException:
            logging.error("Error on open serial connection on {}".format(self._rs232_config.port))
            traceback.print_exception(*sys.exc_info())
            exit(1)

        if not rs232_connection.isOpen():
            rs232_connection.open()

        while True:
            logging.info("Waiting for RS232 client question...")
            client_question = rs232_connection.read(4)
            logging.info("Question received from client: {}".format(client_question.decode()))
            if RS232_EXPECTED_CLIENT_QUESTION == client_question.decode():
                logging.info("Question match with expected. Starting RS232 connection...")
                rs232_connection.write(RS232_ANSWER_TO_CLIENT_QUESTION.encode('utf-8'))
                break
            else:
                logging.info("Question does not match the expected, still waiting for a client...")

        return ServerProtocol(MessageProtocolRS232(rs232_connection))

    def _tcp_wait_connection(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', self._listening_port))
        server_socket.listen(MAX_CONCURRENT_CLIENTS - 1)  # Only handles one client

        logging.debug("[ElectronicInstrumentAdapter][api][start] - proceed to accept new connection")
        socket_connection, addr = server_socket.accept()
        logging.debug('[ElectronicInstrumentAdapter][api][start] - got connection from {}'.format(addr))

        return ServerProtocol(MessageProtocolTCP(socket_connection))
