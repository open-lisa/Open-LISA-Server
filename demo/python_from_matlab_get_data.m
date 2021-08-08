% Es necesario definir la ruta del intérprete de python
pcPythonExe = 'C:\Users\gabro\AppData\Local\Programs\Python\Python39\python.exe';
%[ver, exec, loaded]	= pyversion(pcPythonExe);
pyversion

py.print("Conexi�n con el servidor")
server_ip = "192.168.1.109"
server_port = 8080
eia_sdk = py.electronic_instrument_adapter_sdk.EIA(server_ip, server_port)

try
    py.print("************ Lista de Instrumentos: ************ ")
    instruments = eia_sdk.list_instruments()

    % El ID del oscilloscopio es: USB0::0x0699::0x0363::C107676::INSTR
    
    py.print("************ Ver deatlle de Instrumento: ************ ")
    osciliscopio = eia_sdk.get_instrument("USB0::0x0699::0x0363::C107676::INSTR")

    % Enviamos comandos de configuracion
    
    osciliscopio.send("set_waveform_bytes_width_1")
    osciliscopio.send("set_waveform_encoding_rpbinary")

    % Obtenemos parámetros necesarios para hacer el plot
    ymult = osciliscopio.send("get_waveform_vertical_scale_factor")
    yzero = osciliscopio.send("get_waveform_conversion_factor")
    yoff = osciliscopio.send("get_waveform_vertical_offset")
    xincr = osciliscopio.send("get_waveform_horizontal_sampling_interval")
    
    % Data es una lista de bytes de python (bytes)
    data = uint8(osciliscopio.send("get_waveform_data", "bytes"));
    
    % Casteo a double el header len porque luego indexaremos con eso
    header_len = double(2 + data(2));

    % Descartamos el header y el Ultimo dato
    ADC_wave = data(header_len:end-1);

    volts = (double(ADC_wave) - yoff) * ymult + yzero;
    
    vols_size = size(volts);
    time = 0 : xincr : xincr * (vols_size(2)-1);

    plot(time, volts);
catch e
    fprintf(1,'The identifier was:\n%s',e.identifier);
    fprintf(1,'There was an error! The message was:\n%s',e.message);

    % Es necesario desconectar la SDK explicitamente ya que
    % los destructores de los objetos Python no son llamados
    % Esto se debe a que las variables siguen existiendo en el Workspace de Matlab.
    eia_sdk.disconnect()
end

eia_sdk.disconnect()