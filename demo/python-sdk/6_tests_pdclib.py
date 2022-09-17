import Open_LISA_SDK

try:
    print("test PDC Lib Wrapper")
    sdk = Open_LISA_SDK.SDK(log_level="DEBUG")
    sdk.connect_through_TCP(host="10.147.18.66", port=8080)

    instruments = sdk.get_instruments()

    test_cam_id = None
    for instrument in instruments:
        if instrument["brand"] == "PHOTRON Test":
            test_cam_id = instrument["id"]
            break

    result = sdk.send_command(
        instrument_id=test_cam_id, command_invocation="init")

    print(result)
except Exception as e:
    print("Error")
    print(e)
finally:
    if sdk:
        sdk.disconnect()
