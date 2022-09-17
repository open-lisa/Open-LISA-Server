import Open_LISA_SDK


def bytes_to_ints(bytes, int_size=4, byte_order="little", signed=False):
    result = tuple()

    for i in range(0, len(bytes), int_size):
        int_bytes = bytes[i:i+int_size]
        result += (int.from_bytes(int_bytes,
                   byteorder=byte_order, signed=signed),)

    return result


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

    result_bytes = result["value"]

    print(result_bytes)
    print(type(result_bytes))
    print(len(result_bytes))
    first_num = result_bytes[0:4]
    second_num = result_bytes[4:]
    print(first_num)
    print(second_num)
    byte_order = "little"
    first_num_as_int = int.from_bytes(
        bytes=first_num, byteorder=byte_order, signed=False)
    second_num_as_int = int.from_bytes(
        bytes=second_num, byteorder=byte_order, signed=False)
    print("🚀 ~ file: 6_tests_pdclib.py ~ line 30 ~ first_num_as_int", first_num_as_int)
    print("🚀 ~ file: 6_tests_pdclib.py ~ line 32 ~ second_num_as_int",
          second_num_as_int)

    print(bytes_to_ints(bytes=result_bytes))
except Exception as e:
    print("Error")
    print(e)
finally:
    if sdk:
        sdk.disconnect()
