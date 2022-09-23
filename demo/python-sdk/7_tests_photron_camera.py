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
    sdk = Open_LISA_SDK.SDK(log_level="INFO")
    sdk.connect_through_TCP(host="10.186.223.80", port=8080)

    instruments = sdk.get_instruments()
    print(instruments)

    cam_id = None
    for instrument in instruments:
        if instrument["brand"] == "PHOTRON":
            cam_id = instrument["id"]
            break

    print("cam ID = {}".format(cam_id))

    result = sdk.send_command(instrument_id=cam_id, command_invocation="init")
    result_bytes = result["value"]
    print("init command result bytes = {}".format(result_bytes))
    print("init command result = {}".format(bytes_to_ints(result_bytes)))

    hexa_ip = "C0A8000A"
    camera_ip_as_int = int(hexa_ip, 16)
    print("camera_ip_as_int = {}".format(camera_ip_as_int))
    result = sdk.send_command(instrument_id=cam_id,
                              command_invocation="detect_device {}".format(camera_ip_as_int))
    result_bytes = result["value"]
    print("init command result bytes = {}".format(result_bytes))
    print("init command result = {}".format(bytes_to_ints(result_bytes)))

    # print(type(result_bytes))
    # print(len(result_bytes))
    # first_num = result_bytes[0:4]
    # second_num = result_bytes[4:]
    # print(first_num)
    # print(second_num)
    # byte_order = "little"
    # first_num_as_int = int.from_bytes(
    #     bytes=first_num, byteorder=byte_order, signed=False)
    # second_num_as_int = int.from_bytes(
    #     bytes=second_num, byteorder=byte_order, signed=False)
    # print("🚀 ~ file: 6_tests_pdclib.py ~ line 30 ~ first_num_as_int", first_num_as_int)
    # print("🚀 ~ file: 6_tests_pdclib.py ~ line 32 ~ second_num_as_int",
    #       second_num_as_int)

    # print(bytes_to_ints(bytes=result_bytes))
except Exception as e:
    print("Error")
    print(e)
finally:
    if sdk:
        sdk.disconnect()
