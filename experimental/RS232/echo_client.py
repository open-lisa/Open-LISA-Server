# Connected on COM3
import serial

print("I don't know where my serial connection Server is, so I'll try one by one...")
server_endpoint = ""

for i in range(1, 9):
    endpoint = "COM{}".format(i)
    print("Trying to get an answer from {}".format(endpoint))

    try:
        connection = serial.Serial(endpoint, timeout=3)

        if not connection.isOpen():
            connection.open()

        connection.write(b'ping')

        response = connection.read(4)
        if len(response) > 0:
            print("There is an answer from {}".format(endpoint))
            print(str(response.decode("utf-8")))
            server_endpoint = endpoint
            break
        else:
            print("No answer detected from {}".format(endpoint))

        connection.close()

    except serial.SerialException:
        print("Error on open serial connection on {}".format(endpoint))

if server_endpoint != "":
    print("Server serial connection found on endpoint {}".format(server_endpoint))