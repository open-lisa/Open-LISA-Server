import serial
import logging

TCP_LISTENING_PORT_DEFAULT = 8080
RS232_EXPECTED_CLIENT_QUESTION = 'OPEN'
RS232_ANSWER_TO_CLIENT_QUESTION = 'LISA'


class OpenLisaCommunicationProtocol:

    def __init__(self, rs232_configs, tcp_listening_port=TCP_LISTENING_PORT_DEFAULT):
        self._tcp_listening_port = tcp_listening_port

        self._rs232_baudrate = rs232_configs.baudrate
        self._rs232_port = rs232_configs.port
        self._rs232_timeout = rs232_configs.timeout


    def rs232_wait_connection(self):
        self._rs232_connection = serial.Serial(
            port=self._rs232_port,
            baudrate=self._rs232_baudrate,
            timeout=self._rs232_timeout)

        print(self._rs232_connection)

        if not self._rs232_connection.isOpen():
            self._rs232_connection.open()

        while True:
            logging.info("Waiting for RS232 client question...")
            client_question = self._rs232_connection.read(4)
            logging.info("Question received from client: {}".format(client_question.decode()))
            if RS232_EXPECTED_CLIENT_QUESTION == client_question.decode():
                logging.info("Question match with expected. Starting RS232 connection...")
                break
            else:
                logging.info("Question does not match the expected, still waiting for a client...")

            self._rs232_connection.write(RS232_ANSWER_TO_CLIENT_QUESTION.encode('utf-8'))
