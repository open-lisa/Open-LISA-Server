import Open_LISA_SDK
import time

MATLAB_SCRIPT = "'processing_example.m'"
MATLAB_COMMAND = "matlab -nodisplay -nosplash -nodesktop -r \"run {}; exit;\"".format(MATLAB_SCRIPT)


def main():
    sdk = Open_LISA_SDK.SDK(log_level="DEBUG")
    sdk.connect_through_TCP("localhost", 8080)

    sdk.send_file("./image_input.bmp", "sandbox/image_input.bmp")
    sdk.send_file("./processing_example.m", "sandbox/processing_example.m")
    return_code, stdout, stderr = sdk.execute_bash_command(MATLAB_COMMAND, capture_stdout=True, capture_stderr=True)

    print(return_code)
    print(stdout)
    print(stderr)

    # this sleep is needed because the matlab command is executed instantly, and Popen cant wait until the
    # script finish (limitation of matlab)
    # https://www.mathworks.com/matlabcentral/answers/8031-calling-matlab-from-python-and-have-python-wait-for-matlab-to-finish
    time.sleep(10)

    sdk.get_file("sandbox/image_output.bmp", "image_output_from_remote.bmp")

    sdk.disconnect()


if __name__ == "__main__":
    main()
