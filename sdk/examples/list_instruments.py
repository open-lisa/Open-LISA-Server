import electronic_instrument_adapter_sdk

# Define server config
sdk = electronic_instrument_adapter_sdk.EIA("127.0.0.1", 8080)

# List instruments
print(sdk.list_instruments())
