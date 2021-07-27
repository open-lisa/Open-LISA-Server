% Es necesario definir la ruta del intérprete de python
pcPythonExe = 'C:\Users\gabro\AppData\Local\Programs\Python\Python36\python.exe';
%[ver, exec, loaded]	= pyversion(pcPythonExe);
pyversion

py.print("Conexion con el servidor")
eia_sdk = py.electronic_instrument_adapter_sdk.EIA("127.0.0.1", "8080")

try
    py.print("************ Lista de Instrumentos: ************ ")
    instruments = eia_sdk.list_instruments();

    % El ID del oscilloscop�o es: USB0::0x0699::0x0363::C107676::INSTR
    
    py.print("************ Ver deatlle de Instrumento: ************ ")
    osciliscopio = eia_sdk.get_instrument("USB0::0x0699::0x0363::C107676::INSTR")

    % Enviamos comandos de configuracion
    
    osciliscopio.send("set_waveform_bytes_width_1");
    osciliscopio.send("set_waveform_encoding_rpbinary");

    % Creamos array de numpy para obtener mediciones
    volts = py.numpy.empty(int32(0))

    % Obtenemos parámetros necesarios para hacer el plot
    ymult = osciliscopio.send("get_waveform_vertical_scale_factor", "double");
    yzero = osciliscopio.send("get_waveform_conversion_factor", "double");
    yoff = osciliscopio.send("get_waveform_vertical_offset", "double");
    xincr = osciliscopio.send("get_waveform_horizontal_sampling_interval", "double");

    % Data es un Python bytearray
    data = osciliscopio.send("get_waveform_data", "bytearray")
    
    % Con llaves accedemos a los valores de determinada posicion (Matlab indexa desde 1 a diferencia de Python que es desde 0)
    header_len = 2 + data{2};

    % Descartamos el header y el Ultimo dato
    ADC_wave = data(header_len:end-1);

    % Definimos el formato que se usara para py.struct.unpack
    struct_format = sprintf("%iB", length(ADC_wave));
    ADC_wave = py.numpy.array(py.struct.unpack(struct_format, ADC_wave));
    
    % TODO: Convertir 'ADC_wave' en un array de Matlab para no usar Numpy

    volts = (ADC_wave - yoff) * ymult + yzero;
    
    % TODO: Convertir 'time' en un array de Matlab para no usar Numpy
    
    time = py.numpy.arange(0, xincr * py.len(volts), xincr);

    % Es necesario hacer la siguiente conversion numpy.array --> python native list --> cell matlab --> y convertir los datos a double de la cell
    volts_cell = cell(py.list(volts));
    volts_array = cellfun(@double, volts_cell);
    time_cell = cell(py.list(time));
    time_array = cellfun(@double, time_cell);

    plot(time_array, volts_array);
catch e
    fprintf(1,'The identifier was:\n%s',e.identifier);
    fprintf(1,'There was an error! The message was:\n%s',e.message);

    % Es necesario desconectar la SDK explicitamente ya que
    % los destructores de los objetos Python no son llamados
    % Esto se debe a que las variables siguen existiendo en el Workspace de Matlab.
    eia_sdk.disconnect()
end

eia_sdk.disconnect()