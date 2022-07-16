import json
import logging
import subprocess

from open_lisa.exceptions.base_exception import OpenLISAException

SUCCESS_RESPONSE = "OK"
ERROR_RESPONSE = "ERROR"

COMMAND_GET_INSTRUMENTS = "GET_INSTRUMENTS"
COMMAND_GET_INSTRUMENT = "GET_INSTRUMENT"
COMMAND_GET_INSTRUMENT_COMMANDS = "GET_INSTRUMENT_COMMANDS"
COMMAND_VALIDATE_COMMAND = "VALIDATE_COMMAND"
COMMAND_SEND_COMMAND = "SEND_COMMAND"
COMMAND_DISCONNECT = "DISCONNECT"
COMMAND_SEND_FILE = "SEND_FILE"
COMMAND_GET_FILE = "GET_FILE"
COMMAND_EXECUTE_BASH = "EXECUTE_BASH"


class ServerProtocol:
    def __init__(self, message_protocol):
        self._message_protocol = message_protocol

    def get_command(self):
        return self._message_protocol.receive_msg()

    def handle_get_instruments(self, instruments_repository):
        jsons_string = instruments_repository.get_all_as_json()
        self._message_protocol.send_msg(jsons_string)

    def handle_get_instrument(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_id(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(json.dumps(instrument.to_dict()))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_get_instrument_commands(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_id(id)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(
                json.dumps(instrument.commands_map))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)
            return

    def handle_validate_command(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        command = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_id(id)
            commands_parts = command.split(' ')
            command_name = commands_parts[0]
            command_params = \
                commands_parts[1:] if len(commands_parts) > 1 else []
            instrument.validate_command(command_name, command_params)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_send_command(self, instruments_repository):
        id = self._message_protocol.receive_msg()
        command = self._message_protocol.receive_msg()
        try:
            instrument = instruments_repository.get_by_id(id)
            commands_parts = command.split(' ')
            command_name = commands_parts[0]
            command_params = \
                commands_parts[1:] if len(commands_parts) > 1 else []
            command_execution_result = instrument.send_command(
                command_name, command_params)
            self._message_protocol.send_msg(SUCCESS_RESPONSE)
            self._message_protocol.send_msg(
                json.dumps(command_execution_result.to_dict()))
        except OpenLISAException as e:
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg(e.message)

    def handle_send_file(self):
        file_name = str(self._message_protocol.receive_msg())
        file_bytes = self._message_protocol.receive_msg(decode=False)
        with open(file_name, "wb") as file:
            file.write(file_bytes)

        # TODO: Answer a bytes checksum for error checking
        self._message_protocol.send_msg(SUCCESS_RESPONSE)

    def handle_get_file(self):
        file_name = str(self._message_protocol.receive_msg())
        try:
            with open(file_name, "rb") as file:
                self._message_protocol.send_msg(SUCCESS_RESPONSE)
                data = file.read()
                self._message_protocol.send_msg(data, encode=False)
        except FileNotFoundError as e:
            logging.error(
                "[OpenLISA][ServerProtocol][handle_get_file] Requested file does not exist: {}".format(file_name))
            self._message_protocol.send_msg(ERROR_RESPONSE)
            self._message_protocol.send_msg("File not found: {}".format(file_name))

    def handle_execute_bash_command(self):
        command = str(self._message_protocol.receive_msg())
        should_send_stdout = bool(self._message_protocol.receive_msg())
        should_send_stderr = bool(self._message_protocol.receive_msg())
        logging.info("[OpenLISA][ServerProtocol][execute_bash_command]"
                     " About to execute the following command sent by client: {}"
                     " Must send stdout: {}. Must send stderr: {}"
                     .format(command, should_send_stdout, should_send_stderr))

        execution_command_process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = execution_command_process.communicate()
        return_code = str(execution_command_process.wait())
        logging.info("[OpenLISA][ServerProtocol][execute_bash_command]"
                     " Return code after command execution: {}".format(return_code))

        self._message_protocol.send_msg(return_code)
        if should_send_stdout:
            self._message_protocol.send_msg(stdout.decode())
            logging.info("[OpenLISA][ServerProtocol][execute_bash_command][stdout] {}".format(stdout.decode()))
        if should_send_stderr:
            self._message_protocol.send_msg(stderr.decode())
            logging.info("[OpenLISA][ServerProtocol][execute_bash_command][stderr] {}".format(stderr.decode()))

    def handle_disconnect_command(self):
        self._message_protocol.disconnect()
