import Open_LISA_SDK


def bytes_to_ints(bytes, int_size=4, byte_order="little", signed=False):
    result = tuple()

    for i in range(0, len(bytes), int_size):
        int_bytes = bytes[i:i+int_size]
        result += (int.from_bytes(int_bytes,
                   byteorder=byte_order, signed=signed),)

    return result


try:
    print("Photron Camera Tests")
    sdk = Open_LISA_SDK.SDK(log_level="INFO")
    sdk.connect_through_TCP(host="10.186.223.80", port=8080)

    instruments = sdk.get_instruments()
    print(instruments)

    cam_id = None
    for instrument in instruments:
        if instrument["brand"] == "PHOTRON":
            cam_id = instrument["id"]
            break

    print("Cam ID = {}".format(cam_id))

    # INIT LIBRARY
    result = sdk.send_command(instrument_id=cam_id, command_invocation="init")
    result_bytes = result["value"]
    print("init command result bytes = {}".format(result_bytes))
    print("init command result = {}".format(bytes_to_ints(result_bytes)))

    # DETECT DEVICE
    hexa_ip = "C0A8000A"
    camera_ip_as_int = int(hexa_ip, 16)
    print("camera_ip_as_int = {}".format(camera_ip_as_int))
    result = sdk.send_command(instrument_id=cam_id,
                              command_invocation="detect_device {}".format(camera_ip_as_int))
    result_bytes = result["value"]
    print("detect_device command result bytes = {}".format(result_bytes))
    print("detect_device command result = {}".format(bytes_to_ints(result_bytes)))
    device_detected = bytes_to_ints(result_bytes)
    assert device_detected[0] == 1  # if it is 0 it was an error
    device_code = device_detected[1]
    temp_device_no = device_detected[2]
    device_interface = device_detected[3]

    # OPEN DEVICE
    result = sdk.send_command(instrument_id=cam_id,
                              command_invocation="open_device {} {} {}".format(
                                  device_code, temp_device_no, device_interface))
    result_bytes = result["value"]
    print("open_device command result bytes = {}".format(result_bytes))
    print("open_device command result = {}".format(bytes_to_ints(result_bytes)))
    opened_device = bytes_to_ints(result_bytes)
    # assert device_detected[0] == 1  # if it is 0 it was an error
    device_code = opened_device[1]
    device_no = opened_device[2]

    # DEVICE NAME
    result = sdk.send_command(instrument_id=cam_id,
                              command_invocation="get_device_name {} {}".format(device_no, child_no))
    result_bytes = result["value"]
    # only first 8 bytes represents ints, rest is string
    int_bytes = result_bytes[0:8]
    device_name_bytes = result_bytes[8:]
    print("get_device_name command result bytes = {}".format(result_bytes))
    print("get_device_name command result ints = {}".format(
        bytes_to_ints(int_bytes)))
    print("get_device_name device name bytes = {}".format(
        bytes_to_ints(device_name_bytes)))
    print("get_device_name device name = {}".format(
        bytes_to_ints(device_name_bytes.decode())))

    # CLOSE DEVICE
    result = sdk.send_command(instrument_id=cam_id,
                              command_invocation="close_device {}".format(device_no))
    result_bytes = result["value"]
    print("close_device command result bytes = {}".format(result_bytes))
    print("close_device command result = {}".format(bytes_to_ints(result_bytes)))
except Exception as e:
    print("Error")
    print(e)
finally:
    if sdk:
        sdk.disconnect()
