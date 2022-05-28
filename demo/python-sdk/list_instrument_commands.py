import Open_LISA_SDK

sdk = Open_LISA_SDK.SDK(log_level="DEBUG")
sdk.connect_through_RS232()

# List instruments
instruments = sdk.list_instruments()
print(instruments)

if len(instruments) != 0:
    instrument = instruments[0]
    commands = instrument.available_commands()

    for c in commands:
        print(c)
else:
    print("no instruments available")
