import electronic_instrument_adapter_sdk

# Define server config
sdk = electronic_instrument_adapter_sdk.EIA("127.0.0.1", 8080)

# List instruments
instruments = sdk.list_instruments()

if len(instruments) != 0:
  instrument = instruments[0]

  commands = instrument.available_commands()
  for c in commands:
    print(c)
else:
  print("no instruments available")