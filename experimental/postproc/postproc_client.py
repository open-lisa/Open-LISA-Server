# Connected on COM3
import serial

# REF: https://www.mathworks.com/matlabcentral/answers/102082-how-do-i-call-matlab-from-the-dos-prompt
# El script de matlab debe estar expresado en ruta absoluta
MATLAB_SCRIPT = "'C:\\Users\\FIUBA\\PycharmProjects\\Open-LISA-Server\\experimental\\postproc\\processing_example.m'"
# El intérprete de matlab debe ejecutarse con opciones para que no levante interfaz gráfica
# La opción -r recibe un string con el código que se debe ejecutar
#   El comando run ejecuta un archivo .m
#   El comando exit es necesario para 'cerrar' la consola de matlab
# La opción --logfile sirve para volcar en un archivo los logs de matlab (prints y errores)
MATLAB_COMMAND = "matlab -nodisplay -nosplash -nodesktop -r \"run {}; exit;\" -logfile log.txt".format(MATLAB_SCRIPT)

server_endpoint = ""
connection = None

for i in range(1, 9):
    endpoint = "COM{}".format(i)

    try:
        connection = serial.Serial(endpoint, timeout=3)

        if not connection.isOpen():
            connection.open()

        connection.write("OPEN".encode())

        response = connection.read(4)
        if len(response) > 0 and str(response.decode("utf-8")) == "LISA":
            server_endpoint = endpoint
            break

    except serial.SerialException:
        print("Error on open serial connection on {}".format(endpoint))

if server_endpoint == "":
    print("Server not found")
    exit(1)

print("Server serial connection found on endpoint {}".format(server_endpoint))

print("Size of matlab command: {}".format(len(MATLAB_COMMAND)))
connection.write(MATLAB_COMMAND.encode())
# Tras enviar el comando, podría quedarse esperando el status code de la ejecución
# y el logfile con la salida del intérprete con logs del usuario y detalle de errores

connection.close()
