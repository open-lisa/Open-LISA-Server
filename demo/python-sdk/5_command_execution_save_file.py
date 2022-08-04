import Open_LISA_SDK

def main():
    sdk = Open_LISA_SDK.SDK(log_level="ERROR")
    sdk.connect_through_TCP(host="localhost", port=8080)
    instruments = sdk.get_instruments()
    mocked_camera = instruments[1]


    remote_file_path = "sandbox/remote.jpg"
    command_result = sdk.send_command(
        instrument_id=mocked_camera["id"],
        command_invocation="get_image",
        response_format="BYTES",
        command_result_output_file=remote_file_path
    )

    local_file_path = "./image_from_remote.jpeg"
    sdk.get_file(remote_file_path, local_file_path)

    sdk.disconnect()

if __name__ == "__main__":
    main()
