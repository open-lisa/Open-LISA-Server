# Open-LISA-Server

This program provides services that can be integrated with SDK in node clients
[Open LISA SDK](https://github.com/aalvarezwindey/Open-LISA-SDK).

## Dependencies

1. Python 3
2. Python libraries `pyvisa`, `pyvisa-py`, `pyserial`, `python-dotenv`, `pysondb`
   (for test purposes)
3. Python libraries in order to run tests: `pytest`, `pytest-cov`, `open-lisa-sdk`.
4. Drivers for each instrument that want to be controlled (provided by manufacturer)
5. C compiler (in order to generate dll's for integration with some instruments)

## Run tests

Unit and integration tests can be executed by the following command, relative to root of this project:

```bash
$ sh ./run_tests.sh
```

at the end of the process, test coverage and other metrics will be reported.

## Run server

Server can be executed by the following command:

```bash
$ python ./main.py
```

If you run it like the example above, you will get the message asking for correct invocation:

```
usage: Optional app description [-h] --mode {SERIAL,TCP} [--rs_232_port RS_232_PORT] [--tcp_port TCP_PORT] [--rs_232_baudrate RS_232_BAUDRATE] [--rs_232_timeout RS_232_TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  --mode {SERIAL,TCP}   SERIAL or TCP
  --rs_232_port RS_232_PORT
                        RS232 connection port, i.e. COM3
  --tcp_port TCP_PORT   TCP Listening port, i.e. 8080
  --rs_232_baudrate RS_232_BAUDRATE
                        Baudrate of RS232 connection, i.e. 19200
  --rs_232_timeout RS_232_TIMEOUT
                        Timeout in seconds for RS232 connection reads
```

### Run server in Serial mode

```bash
python .\main.py --mode SERIAL --rs_232_port COM6 --env test --log-level DEBUG
```
Will run server using test databases in RS-232 Serial mode, waiting clients to communicate in channel COM6.

### Run server in TCP mode

Disclaimer: No security concerns were considered in TCP mode (such as authentication or encryption). Use this mode only
if you can't use Serial mode. 

```bash
python main.py  --env production --mode TCP --tcp_port 8080 --log-level INFO
```

Will run server using productive databases in TCP-socket mode, listening connections in 8080 port.

## Admin

This project has a [UI Admin](https://github.com/aalvarezwindey/Open-LISA-UI) that allows the creation, deletion and
modification of instruments and commands. In addition, allows the manipulation of the user file system in this Server
(files in data, data_test and data_dev folders).

## C Libraries

Some instruments don't support SCPI protocol, and the manufacturers provides custom libraries instead. Usually, those
libraries can be imported and used in C language. This project allows user to integrate this kind of intruments, if
compiles a custom C program with the primitives that going to control the instrument, with a .dll file as target.

### Unix / OSX

```
gcc -c -Wall -Werror -fpic <.c file>
```

Will generate .o file.

```
gcc -shared -o <.so output file> <.o file>
```

This will generate a .so file, a unix / osx equivalent to .dll in Windows.

### Windows

```
gcc -c -Wall -fpic <.c file>
```

Will generate .o file.

```
gcc -shared -o <.dll output file> <.o file>
```

This will generate a .dll file.
