import electronic_instrument_adapter_sdk
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, help="server host", default="127.0.0.1")
parser.add_argument("--port", type=int, help="server port", default=8080)
args = parser.parse_args()

# Define server config
sdk = electronic_instrument_adapter_sdk.EIA(args.host, args.port)

# List instruments
print(sdk.list_instruments())
