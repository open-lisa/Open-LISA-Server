import Open_LISA_SDK
from timeit import default_timer as timer

sdk = Open_LISA_SDK.SDK()
sdk.connect_through_RS232()

# List instruments
start = timer()
instruments = sdk.list_instruments()
end = timer()
print("Get instruments elapsed time: {}".format(end - start))
print(instruments)

if len(instruments) != 0:
  instrument = instruments[0]

  start = timer()
  commands = instrument.available_commands()
  end = timer()
  print("Get available commands elapsed time: {}".format(end - start))

  for c in commands:
    print(c)
else:
  print("no instruments available")