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

    py.print("************ Ver comandos disponibles para Instrumento: ************ ")
    osciliscopio.available_commands()
    
    py.print("*********** Check invalid command to instrument ************");
    osciliscopio.validate_command("pepinardovich")
    
    py.print("*********** Check valid command configuration to instrument ************");
    osciliscopio.validate_command("set_waveform_encoding_ascii")
    
    py.print("*********** Check invalid command configuration with parameters ************");
    osciliscopio.validate_command("set_trigger_level 10 20")
    
    py.print("*********** Check invalid command configuration parameter type ************");
    osciliscopio.validate_command("set_trigger_level ASCII")
    
    py.print("*********** Check valid command configuration with parameter ************");
    osciliscopio.validate_command("set_trigger_level 3.4")

catch e
    fprintf(1,'The identifier was:\n%s',e.identifier);
    fprintf(1,'There was an error! The message was:\n%s',e.message);
    eia_sdk.disconnect()
end

eia_sdk.disconnect()