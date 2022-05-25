#!/usr/bin/env python3
import argparse
import logging

from electronic_instrument_adapter.api import ElectronicInstrumentAdapter
from electronic_instrument_adapter.protocol.rs232configuration import RS232Configuration


def parse_config_params():
    """ Parse env variables to find program config params
    Function that search and parse program configuration parameters in the
    program environment variables. If at least one of the config parameters
    is not found a KeyError exception is thrown. If a parameter could not
    be parsed, a ValueError is thrown. If parsing succeeded, the function
    returns a map with the env variables
    """
    parser = argparse.ArgumentParser("Optional app description")
    parser.add_argument('--mode', required=True, help='SERIAL or TCP', choices=['SERIAL', 'TCP'])
    parser.add_argument('--rs_232_port', help='RS232 connection port, i.e. COM3')
    parser.add_argument('--tcp_port', type=int, help='TCP Listening port, i.e. 8080')
    parser.add_argument('--rs_232_baudrate', type=int, help='Baudrate of RS232 connection, i.e. 19200')
    parser.add_argument('--rs_232_timeout', type=int, help='Timeout in seconds for RS232 connection reads')

    args = parser.parse_args()
    if args.mode == "SERIAL" and args.rs_232_port is None:
        logging.error("Serial port must be specified in Serial mode")
        exit(1)
    if args.mode == "TCP" and args.tcp_port is None:
        logging.error("Port must be specified in TCP mode")
        exit(1)

    return parser.parse_args()


def initialize_log():
    """
    Python custom logging initialization
    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """

    logging.basicConfig(
        format='%(asctime)s [EIA_SERVER] %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def main():
    initialize_log()
    args = parse_config_params()

    rs232_config = RS232Configuration(args.rs_232_port, args.rs_232_baudrate, args.rs_232_timeout)

    eia_server = ElectronicInstrumentAdapter(
        mode=args.mode,
        rs232_config=rs232_config,
        listening_port=args.tcp_port
    )
    eia_server.start()


if __name__ == "__main__":
    main()
