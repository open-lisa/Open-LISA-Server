#!/usr/bin/env python3
import sys
import logging
import json
from json import JSONDecodeError

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
        format='%(asctime)s [OPEN_LISA_SPECS_VALIDATOR] %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    initialize_log()

    if len(sys.argv) != 2:
        logging.error("Instrument spec json file is expected as parameter.")
        logging.info("Invocation example: '$ python validate_specs.py tektronix_tds1002b_cmd.json'")
        exit(ERROR_CODE)

    with open(sys.argv[SPECS_FILE_ARG_POSITION]) as file:
        try:
            specs_file = json.load(file)
        except JSONDecodeError as e:
            logging.error("Invalid json format: {}".format(e))
            exit(ERROR_CODE)

        for command, specs in specs_file.items():
            if "command" not in specs:
                handle_error_mandatory_key_not_found(command, "command")
            else:
                if not isinstance(specs["command"], str) or len(specs["command"]) <= 0:
                    handle_error_invalid_format(command, "command", "string")
                params_qty = specs["command"].count("{}")
                if params_qty > 0:
                    if "params" not in specs:
                        handle_error_conditional_key_not_found(command, "params")
                    else:
                        for param in specs["params"]:
                            if "position" not in param:
                                handle_error_conditional_key_not_found(command, 'params["position"]')
                            else:
                                if not isinstance(param["position"], int):
                                    handle_error_invalid_format(command, 'params["position"]', "int")
                            if "type" not in param:
                                handle_error_conditional_key_not_found(command, 'params["type"]')
                            else:
                                if not isinstance(param["type"], str) or len(param["type"]) <= 0:
                                    handle_error_invalid_format(command, 'params["type"]', "string")
                            if "example" not in param:
                                handle_error_conditional_key_not_found(command, 'params["example"]')
                            else:
                                if not isinstance(param["example"], str) or len(param["example"]) <= 0:
                                    handle_error_invalid_format(command, 'params["example"]', "string")
                            if "description" not in param:
                                handle_error_conditional_key_not_found(command, 'params["description"]')
                            else:
                                if not isinstance(param["description"], str) or len(param["description"]) <= 0:
                                    handle_error_invalid_format(command, 'params["description"]', "string")

            if "type" not in specs:
                handle_error_mandatory_key_not_found(command, "type")
            else:
                if not isinstance(specs["type"], str) or len(specs["type"]) <= 0:
                    handle_error_invalid_format(command, "type", "string")
                if specs["type"] not in ("set", "query", "query_buffer"):
                    handle_error_invalid_value(command, "type", ("set", "query", "query_buffer"))

            if "description" not in specs:
                handle_error_mandatory_key_not_found(command, "description")
            else:
                if not isinstance(specs["description"], str) or len(specs["description"]) <= 0:
                    handle_error_invalid_format(command, "description", "string")

    if len(errors) > 0:
        logging.error('\n'.join(map(str, errors)))
        exit(ERROR_CODE)

    logging.info("The specs json file {} is valid.".format(sys.argv[SPECS_FILE_ARG_POSITION]))
    exit(SUCCESSFUL_CODE)


def handle_error_mandatory_key_not_found(command, key):
    error_message = "[COMMAND: {}] Mandatory key '{}' not found".format(command, key)
    logging.debug(error_message)
    errors.append(error_message)


def handle_error_conditional_key_not_found(command, key):
    error_message = "[COMMAND: {}] Conditional key '{}' not found".format(command, key)
    logging.debug(error_message)
    errors.append(error_message)


def handle_error_invalid_format(command, key, correct_format):
    error_message = "[COMMAND: {}] [KEY: {}] Key has an invalid format. It must be {}".format(command, key, correct_format)
    logging.debug(error_message)
    errors.append(error_message)


def handle_error_invalid_value(command, key, valid_values):
    error_message = "[COMMAND: {}] [KEY: {}] Key has an invalid value. Valid values are {}".format(command, key, valid_values)
    logging.debug(error_message)
    errors.append(error_message)


if __name__ == "__main__":
    main()
