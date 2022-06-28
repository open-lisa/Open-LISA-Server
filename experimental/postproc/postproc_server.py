# Connected on COM4
import serial
import os

# Hardcodeo del size en cantidad de bytes del comando a ejecutar indicado por el cliente
# Esto en Open LISA sería transparente gracias al protocolo
COMMAND_EXPECTED_SIZE = 164

connection = serial.Serial("COM4")
if not connection.isOpen():
    connection.open()

handshake = connection.read(4)

if handshake.decode("utf-8") == "OPEN":
    connection.write("LISA".encode('utf-8'))

command = connection.read(COMMAND_EXPECTED_SIZE).decode("utf-8")
print("command received from client: {}".format(command))

# La proxima linea debería estar securizada en Open LISA para que no se pueda enviar
# cualquier comando
return_code = os.system(command)
print("Return code after execute matlab script: {}".format(return_code))

# En esta instancia, el servidor podría devolver al cliente el return_code ...
# ... para evaluar la ejecución del comando de matlab.
# Adicionalmente, podría enviar el logfile donde el usuario pudo haber escrito ...
# ... logs de interés, o donde podrá ver el detalle de los errores del intérprete.
connection.close()
