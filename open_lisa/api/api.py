import serial
import socket
import traceback
import sys

from ..protocol.message_protocol_rs232 import MessageProtocolRS232
from ..protocol.message_protocol_tcp import MessageProtocolTCP
from ..protocol.server_protocol import *
from ..repositories.commands_repository import CommandsRepository

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
        self._server_socket = None
        self._instruments_repository = InstrumentRepository()
        self._commands_repository = CommandsRepository()
        self._shutdown_after_next_client_connection = False  # Do something better than this

    def start(self):
        while True:
            logging.info("Waiting for client connection...")
            if self._mode == MODE_SERIAL:
                try:
                    self._server_protocol = self._rs232_wait_connection()
                except Exception as e:
                    logging.error(
                        "Error in RS232 connection protocol: {}".format(e))
                    continue
            elif self._mode == MODE_TCP:
                self._server_protocol = self._tcp_wait_connection()
            else:
                logging.error(
                    "OpenLisa started with invalid mode: {}".format(self._mode))
                exit(1)

            while True:
                try:
                    logging.info(
                        "[OpenLISA][api][start] - waiting for client command")
                    command = self._server_protocol.get_command()
                    logging.info(
                        "[OpenLISA][api][start] - command received: " + command)
                    if command == COMMAND_HEALTH_CHECK:
                        logging.debug(
                            "[OpenLISA][api][start] - client ask for health check")
                        self._server_protocol.handle_health_check()
                    elif command == COMMAND_GET_INSTRUMENTS:
                        logging.debug(
                            "[OpenLISA][api][start] - getting instruments")
                        self._server_protocol.handle_get_instruments(
                            self._instruments_repository)
                    elif command == COMMAND_GET_INSTRUMENT:
                        logging.debug(
                            "[OpenLISA][api][start] - getting specific instrument")
                        self._server_protocol.handle_get_instrument(
                            self._instruments_repository)
                    elif command == COMMAND_GET_DETECTED_PHYSICAL_ADDRESSES:
                        logging.debug(
                            "[OpenLISA][api][start] - getting detected physical addresses")
                        self._server_protocol.handle_get_detected_physical_addresses(
                            self._instruments_repository)
                    elif command == COMMAND_CREATE_INSTRUMENT:
                        logging.debug(
                            "[OpenLISA][api][start] - creating new instrument")
                        self._server_protocol.handle_create_instrument(
                            self._instruments_repository)
                    elif command == COMMAND_UPDATE_INSTRUMENT:
                        logging.debug(
                            "[OpenLISA][api][start] - updating instrument")
                        self._server_protocol.handle_update_instrument(
                            self._instruments_repository)
                    elif command == COMMAND_DELETE_INSTRUMENT:
                        logging.debug(
                            "[OpenLISA][api][start] - deleting instrument")
                        self._server_protocol.handle_delete_instrument(
                            self._instruments_repository)
                    elif command == COMMAND_GET_INSTRUMENT_COMMANDS:
                        logging.debug(
                            "[OpenLISA][api][start] - getting instrument commands")
                        self._server_protocol.handle_get_instrument_commands(
                            self._instruments_repository)
                    elif command == COMMAND_VALIDATE_COMMAND:
                        logging.debug(
                            "[OpenLISA][api][start] - validating instrument command")
                        self._server_protocol.handle_validate_command(
                            self._instruments_repository)
                    elif command == COMMAND_SEND_COMMAND:
                        logging.debug(
                            "[OpenLISA][api][start] - sending command to instrument")
                        self._server_protocol.handle_send_command(
                            self._instruments_repository)
                    elif command == COMMAND_SEND_FILE:
                        logging.debug(
                            "[OpenLISA][api][start] - receiving file from client")
                        self._server_protocol.handle_send_file()
                    elif command == COMMAND_GET_FILE:
                        logging.debug(
                            "[OpenLISA][api][start] - sending file to client")
                        self._server_protocol.handle_get_file()
                    elif command == COMMAND_DELETE_FILE:
                        logging.debug(
                            "[OpenLISA][api][start] - deleting file")
                        self._server_protocol.handle_delete_file()
                    elif command == COMMAND_GET_DIRECTORY_STRUCTURE:
                        logging.debug(
                            "[OpenLISA][api][start] - getting directory structure")
                        self._server_protocol.handle_get_directory_structure()
                    elif command == COMMAND_EXECUTE_BASH:
                        logging.debug(
                            "[OpenLISA][api][start] - executing bash command sending by client")
                        self._server_protocol.handle_execute_bash_command()
                    elif command == COMMAND_DISCONNECT:
                        logging.info(
                            "[OpenLISA][api][start] - client order disconnect")
                        # self._server_protocol.handle_disconnect_command()
                        break
                    elif command == COMMAND_CREATE_INSTRUMENT_COMMAND:
                        logging.info(
                            "[OpenLISA][api][start] - client order create instrument command")
                        self._server_protocol.handle_create_instrument_command(
                            self._commands_repository, self._instruments_repository)
                    elif command == COMMAND_DELETE_INSTRUMENT_COMMAND:
                        logging.info(
                            "[OpenLISA][api][start] - client order delete instrument command")
                        self._server_protocol.handle_delete_instrument_command(
                            self._commands_repository)
                    elif command == COMMAND_CREATE_DIRECTORY:
                        logging.info(
                            "[OpenLISA][api][start] - client order create directory")
                        self._server_protocol.handle_create_directory()
                    elif command == COMMAND_DELETE_DIRECTORY:
                        logging.info(
                            "[OpenLISA][api][start] - client order delete directory")
                        self._server_protocol.handle_delete_directory()
                    elif command == COMMAND_SET_INSTRUMENT_VISA_ATTRIBUTE:
                        logging.info(
                            "[OpenLISA][api][start] - client order set visa attribute")
                        self._server_protocol.handle_set_instrument_visa_attribute(
                            self._instruments_repository)
                    elif command == COMMAND_GET_INSTRUMENT_VISA_ATTRIBUTE:
                        logging.info(
                            "[OpenLISA][api][start] -  client order get visa attribute")
                        self._server_protocol.handle_get_instrument_visa_attribute(
                            self._instruments_repository)
                    elif command == COMMAND_RESET_DATABASES:
                        self._server_protocol.handle_reset_databases()
                    else:
                        logging.error(
                            "[OpenLISA][api][start] - unknown command '{}'".format(command))
                except ConnectionResetError as ex:
                    logging.info(
                        "[OpenLISA][api][start] - client disconnected {}".format(ex))
                    break
                except Exception as ex:
                    logging.error(
                        "[OpenLISA][api][start][UNEXPECTED_ERROR]: {}".format(ex))
                    traceback.print_exc()
                    if self._server_protocol:
                        self._server_protocol.notify_unexpected_server_error_to_client(
                            msg=str(ex))

            if self._shutdown_after_next_client_connection:
                break

    def _rs232_wait_connection(self):
        if not self._rs232_connection:
            self._rs232_create_connection()

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
            logging.error("Error on open serial connection on {}".format(
                self._rs232_config.port))
            traceback.print_exception(*sys.exc_info())
            exit(1)

        if not self._rs232_connection.is_open:
            self._rs232_connection.open()

    def _tcp_wait_connection(self):
        if not self._server_socket:
            self._server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.bind(('', self._listening_port))
            # Only handles one client
            self._server_socket.listen(MAX_CONCURRENT_CLIENTS - 1)

        logging.debug(
            "[OpenLISA][api][start] - TPC proceed to accept new connection")
        socket_connection, addr = self._server_socket.accept()
        logging.debug(
            '[OpenLISA][api][start] - TCP got connection from {}'.format(addr))

        return ServerProtocol(MessageProtocolTCP(socket_connection))
