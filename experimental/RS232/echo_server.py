# Connected on COM4
import serial

connection = serial.Serial("COM4")
if not connection.isOpen():
    connection.open()

x = connection.read(4)

print("received from client: {}".format(x.decode("utf-8")))

connection.write(b'pong')

connection.close()
