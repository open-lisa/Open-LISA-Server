# Manual – Configuración del servidor

## Dependencias

Se recomienda correr el servidor en Sistemas Operativos Microsoft Windows. La primera versión fue probada en Windows 10. Además se debe tener instalado:

- Python 3
- [`pyvisa`](https://pyvisa.readthedocs.io/en/latest/)
- Compilador C en caso de requerir instrumentos que se integren a través de este lenguaje
- Drivers indicados por los fabricantes de los instrumentos a integrar

## Ejecución

Ubicado en el directorio `server` ejecutar:

```bash
python main.py
```

## Registrar un nuevo instrumento

Agregar una nueva entrada en el archivo de instrumentos `open_lisa/instrument/instruments.json`

```json
{
  "brand": "tektronix",
  "model": "tds1002b",
  "description": "Osciloscopio principal",
  "command_file": "tektronix_tds1002b_cmd.json",
  "id": "USB0::0x0699::0x0363::C107676::INSTR"
}
```

De donde:

| Campo          | Descripción                                           |
| -------------- | ----------------------------------------------------- |
| `brand`        | Marca del instrumento                                 |
| `model`        | Modelo del instrumento                                |
| `description`  | Texto libre como descripción a fines de documentación |
| `command_file` | Archivo de configuración de los comandos disponibles  |
| `id`           | Dirección física del instrumento                      |

Para verificar el registro exitoso debemos ver la información del instrumento impresa por pantalla al ejecutar el servidor.

## Agregar comandos al instrumento

Para agregar comandos al instrumento se debe agregar un archivo con el nombre indicado en el campo `command_file` del archivo anterior en la carpeta `open_lisa/instrument/specs`. Por ejemplo:

### Comandos SCPI

A un instrumento que cumple con el protocolo SCPI se le pueden registrar los comandos con un archivo JSON con el siguiente formato

```json
{
  "get_is_in_acquisitions_state": {
    "command": "*OPC?",
    "type": "query",
    "description": "Ask if it's in acquisitions state"
  },
  "set_trigger_level": {
    "command": "TRIGger:MAIn:LEVel {}",
    "type": "set",
    "description": "Sets de oscilloscope edge and pulse width trigger level.",
    "params": [
      {
        "position": 1,
        "type": "float",
        "example": "1.4",
        "description": "Main trigger level, in volts."
      }
    ]
  },
  "get_waveform_data": {
    "command": "CURVE?",
    "type": "query_buffer",
    "description": "Transfers oscilloscope waveform data to and from the oscilloscope in binary or ASCII format. Each waveform that is transferred has an associated waveform preamble that contains information such as data format and scale."
  }
}
```

Donde:

- `get_is_in_acquisitions_state` es el nombre del comando o función que invocará el cliente a través de la SDK.
- `command` corresponde al comando SCPI indicado en el manual del instrumento.
- `type` indica el tipo de comando, los tipos soportados son:
  - `query`: comando de consulta que se espera que devuelva un valor de interés
  - `set`: comando para establecer un valor en el instrumento (a la SDK cliente se le envía la cantidad de bytes enviados al instrumento)
  - `query_buffer`: comando para leer del buffer de datos del instrumento (por debajo utiliza la función `read_raw` del módulo `pyvisa`)
  - `clib`: ver sección siguiente
- `description`: campo con fines documentativos para el comando
- `params`: listado opcional de parámetros que recibe el comando, la cantidad de parámetros se condice con la cantidad de _placeholders_ `{}` que tiene el campo `command`:
  - `position`: indica la posición del argumento recibido (iniciando en 1 y contando según lo enviado por el cliente de izquierda a derecha)
  - `type`: tipo de dato del parámetro. Tipos soportados son: `float`, `int`, `string`.
  - `example`: ejemplo del valor que se espera en el parámetro. Este campo tieen fines informativos para el cliente en caso de ejecutar un comando equívocamente.
  - `description`: campo con fines documentativos para el parámetro.

### Integración con código C

Es común en la industria que determinados instrumentos no cumplan con el protocolo SCPI en cuyos casos los fabricantes proveen sus propias SDKs para integrarse con el instrumento. Las SDKs suelen estar implementadas en lenguajes de bajo nivel como C, es por esto que se pueden registrar comandos cuya función este implementada en dicho lenguaje. Por ejemplo:

```json
{
  "init_cammera": {
    "command": "init",
    "type": "clib",
    "lib_path": "/absolute-path-for-lib/lib.so",
    "description": "Provide a full description of what this command intends to do",
    "params": [
      {
        "position": 1,
        "type": "int",
        "example": "5",
        "description": "Documentation for param"
      },
      {
        "position": 2,
        "type": "float",
        "example": "5.0",
        "description": "Documentation for param"
      }
    ],
    "return": {
      "type": "int",
      "description": "Provide an explanation of return values for documentation purposes"
    }
  },
  "get_image": {
    "command": "get_image",
    "type": "clib",
    "lib_path": "/absolute-path-for-lib/lib.so",
    "description": "Provide a full description of what this command intends to do",
    "return": {
      "type": "bytes",
      "description": "Provide an explanation of return values for documentation purposes"
    }
  }
}
```

Diferencias a tener en cuenta con el formato de los comandos SCPI:

- `init_cammera` en el primer ejemplo corresponde al comando que envía el cliente a través de la Open-LISA-SDK y `command` corresponde a la función C expuesta por la librería.
- `lib_path` ruta a la librería C (`.so` para sistemas Unix o `.dll` para sistemas Windows). Se recomienda que sea la ruta absoluta.
- `return` indica el tipo de dato devuelto por la función C. Valores soportados actualmente `int`, `float` y `bytes`. Para el último caso es necesario que la función C expuesta por la librería reciba un último argumento del tipo `char *`. Esto es necesario ya que para la integración entre Python y C para el caso de este tipo de dato de retorna se utiliza un archivo binario temporal cuya ruta es indicado en este parámetro adicional y es donde debe ser escrito el resultado a retornar al client (como por ejemplo bytes correspondientes a imágenes capturadas por una cámara)
