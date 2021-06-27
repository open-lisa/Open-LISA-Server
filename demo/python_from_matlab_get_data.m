pcPythonExe = 'C:\Users\gabro\AppData\Local\Programs\Python\Python39\python.exe';
%[ver, exec, loaded]	= pyversion(pcPythonExe);
pyversion

py.print("Conexión con el servidor")
eia_sdk = py.instruments.connect("127.0.0.1", 8080)

try
    py.print("************ Lista de Instrumentos: ************ ")
    instruments = eia_sdk.list_instruments()

    % El ID del oscilloscopío es: USB0::0x0699::0x0363::C107676::INSTR
    
    py.print("************ Ver deatlle de Instrumento: ************ ")
    osciliscopio = eia_sdk.get_instrument("USB0::0x0699::0x0363::C107676::INSTR")

    osciliscopio.send("set_waveform_source_ch1")
    osciliscopio.send("set_waveform_bytes_width_1")
    osciliscopio.send("set_waveform_encoding_rpbinary")
    
    volts = py.numpy.empty(int32(0))
    ymult = py.float(osciliscopio.send("get_waveform_vertical_scale_factor"))
    yzero = py.float(osciliscopio.send("get_waveform_conversion_factor"))
    yoff = py.float(osciliscopio.send("get_waveform_vertical_offset"))
    xincr = py.float(osciliscopio.send("get_waveform_horizontal_sampling_interval"))

    data = osciliscopio.send("get_waveform_data");
    
    % Con llaves accedemos a los valores
    header_len = 2 + data{2}

    ADC_wave = data(header_len:end-1)
   
    struct_format = sprintf("%iB", length(ADC_wave));
    ADC_wave = py.numpy.array(py.struct.unpack(struct_format, ADC_wave));
    
    volts = py.numpy.append(volts, (ADC_wave - yoff) * ymult + yzero)
    
    time = py.numpy.arange(0, xincr * py.len(volts), xincr)
    
    volts_cell = cell(py.list(volts))
    volts_array = cellfun(@double, volts_cell)
    
    time_cell = cell(py.list(time))
    time_array = cellfun(@double, time_cell)
    
    plot(time_array, volts_array)
   
    
    
catch e
    fprintf(1,'The identifier was:\n%s',e.identifier);
    fprintf(1,'There was an error! The message was:\n%s',e.message);
    eia_sdk.disconnect()
end

eia_sdk.disconnect()