#!/usr/bin/env python3
import sys
import logging
import json
from json import JSONDecodeError
import os.path

INSTRUMENTS_JSON_FILE = 'instruments.json'
SPECS_FILE_ARG_POSITION = 1
ERROR_CODE = 1
SUCCESSFUL_CODE = 0

errors = []


def initialize_log():
    """
    Python custom logging initialization
    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """

    logging.basicConfig(
        format='%(asctime)s [EIA_INSTRUMENTS_VALIDATOR] %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    initialize_log()

    with open(INSTRUMENTS_JSON_FILE) as file:
        try:
            instruments_file = json.load(file)
        except JSONDecodeError as e:
            logging.error("Invalid json format: {}".format(e))
            exit(ERROR_CODE)

        if len(instruments_file) <= 0:
            logging.error("The instruments file is empty")
            sys.exit(ERROR_CODE)

        index = 1
        for instrument in instruments_file:
            if "brand" not in instrument:
                handle_error_mandatory_key_not_found(index, "brand")
            else:
                if not isinstance(instrument["brand"], str) or len(instrument["brand"]) <= 0:
                    handle_error_invalid_format(index, "brand", "string")
            if "model" not in instrument:
                handle_error_mandatory_key_not_found(index, "model")
            else:
                if not isinstance(instrument["model"], str) or len(instrument["model"]) <= 0:
                    handle_error_invalid_format(index, "model", "string")
            if "description" not in instrument:
                handle_error_mandatory_key_not_found(index, "description")
            else:
                if not isinstance(instrument["description"], str) or len(instrument["description"]) <= 0:
                    handle_error_invalid_format(index, "description", "string")
            if "command_file" not in instrument:
                handle_error_mandatory_key_not_found(index, "command_file")
            else:
                if not isinstance(instrument["command_file"], str) or len(instrument["command_file"]) <= 0:
                    handle_error_invalid_format(index, "command_file", "string")
                else:
                    if not os.path.isfile('specs/' + instrument["command_file"]):
                        handle_error_command_file_not_found(index, instrument["command_file"])

            if "id" not in instrument:
                handle_error_mandatory_key_not_found(index, "id")
            else:
                if not isinstance(instrument["id"], str) or len(instrument["id"]) <= 0:
                    handle_error_invalid_format(index, "id", "string")

            index = index + 1

    if len(errors) > 0:
        logging.error('\n'.join(map(str, errors)))
        exit(ERROR_CODE)

    logging.info("The instruments json file is valid")
    exit(SUCCESSFUL_CODE)


def handle_error_mandatory_key_not_found(index, key):
    error_message = "[INSTRUMENT {}] Mandatory key '{}' not found".format(index, key)
    logging.debug(error_message)
    errors.append(error_message)


def handle_error_invalid_format(index, key, correct_format):
    error_message = "[INSTRUMENT: {}] [KEY: {}] Key has an invalid format. It must be {}".format(index, key, correct_format)
    logging.debug(error_message)
    errors.append(error_message)

def handle_error_command_file_not_found(index, file):
    error_message = "[INSTRUMENT: {}] The command file {} is not found".format(index, file)
    logging.debug(error_message)
    errors.append(error_message)


if __name__ == "__main__":
    main()
