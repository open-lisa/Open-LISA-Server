pcPythonExe = 'C:\Users\gabro\AppData\Local\Programs\Python\Python39\python.exe';
%[ver, exec, loaded]	= pyversion(pcPythonExe);
pyversion

py.list({'This','is a','list'})

py.print("Hello, Python!")

%import py.electronic_instrument_adapter_sdk.*
py.command.do_list()