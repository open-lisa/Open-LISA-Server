% Es necesario definir la ruta del intÃ©rprete de python
pcPythonExe = 'C:\Users\gabro\AppData\Local\Programs\Python\Python39\python.exe';
%[ver, exec, loaded]	= pyversion(pcPythonExe);
pyversion

py.print("Conexión con el servidor")
%server_ip = "192.168.1.109"
server_ip = "localhost"
server_port = 8080
eia_sdk = py.electronic_instrument_adapter_sdk.EIA(server_ip, server_port)

try
    py.print("************ Lista de Instrumentos: ************ ")
    instruments = eia_sdk.list_instruments()

    % El ID del oscilloscopio es: USB0::0x0699::0x0363::C107676::INSTR
    
    py.print("************ Ver deatlle de Instrumento: ************ ")
    camera = eia_sdk.get_instrument("CAM_ID")

    py.print("************ Ver comandos disponibles para Instrumento: ************ ")
    camera.available_commands()
    
    py.print("************ Obtener imagen: ************ ")
    image = uint8(camera.send("get_image", "bytes"));
    class(image)
    
    py.print("************ Guardando imagen imagen ************ ")
    fout = fopen("imagen.jpg", 'wb') ;
    fwrite(fout, image);  
    fclose(fout);
    
catch e
    fprintf(1,'The identifier was:\n%s',e.identifier);
    fprintf(1,'There was an error! The message was:\n%s',e.message);

    % Es necesario desconectar la SDK explicitamente ya que
    % los destructores de los objetos Python no son llamados
    % Esto se debe a que las variables siguen existiendo en el Workspace de Matlab.
    eia_sdk.disconnect()
end

eia_sdk.disconnect()