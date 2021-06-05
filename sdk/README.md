# Electronic Instrument Adapter SDK

Para activar el entorno virtual de la SDK desde la carpeta `sdk` ejecutar:
```
source venv/bin/activate
```


## Build

Desde la carpeta `sdk` ejecutar:
```
python3 setup.py bdist_wheel
```

## Instalación

Desde la carpeta `sdk` ejecutar:
```
pip install dist/*.whl --force-reinstall
```