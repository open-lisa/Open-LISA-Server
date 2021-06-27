#!/bin/bash

source venv/bin/activate
pip install wheel
python3 setup.py bdist_wheel
pip install dist/*.whl --force-reinstall