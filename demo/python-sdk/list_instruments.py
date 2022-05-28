import Open_LISA_SDK

# Define server config
sdk = Open_LISA_SDK.SDK()
sdk.connect_through_RS232()

# List instruments
print(sdk.list_instruments())