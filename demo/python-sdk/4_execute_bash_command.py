import Open_LISA_SDK

MATLAB_SCRIPT = "'C:\\Users\\FIUBA\\PycharmProjects\\Open-LISA-Server\\data_test\\user\\sandbox\\processing_example.m'"
MATLAB_COMMAND = "matlab -nodisplay -nosplash -nodesktop -r \"run {}; exit;\"".format(MATLAB_SCRIPT)


def main():
    sdk = Open_LISA_SDK.SDK(log_level="DEBUG")
    sdk.connect_through_TCP("localhost", 8080)

    sdk.send_file("./image_input.bmp", "sandbox/image_input.bmp")
    sdk.send_file("./processing_example.m", "sandbox/processing_example.m")
    return_code, stdout, stderr = sdk.execute_bash_command(MATLAB_COMMAND, True, True)

    print(return_code)
    print(stdout)
    print(stderr)

    sdk.disconnect()


if __name__ == "__main__":
    main()
