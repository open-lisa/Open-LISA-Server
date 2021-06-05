import electronic_instrument_adapter_sdk

# Define server config
sdk = electronic_instrument_adapter_sdk.EIA("http://192.168.0.172", 8080)

# List instruments
print(sdk.list_instruments())
