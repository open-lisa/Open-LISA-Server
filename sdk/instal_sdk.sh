#!/bin/bash

source venv/bin/activate
pip install wheel
python setup.py bdist_wheel
pip install dist/electronic_instrument_adapter_sdk-0.1.0-py3-none-any.whl --force-reinstall