# Example for creating a python lib:
# https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

from setuptools import find_packages, setup
import pathlib
import os

root = pathlib.Path(__file__).parent
os.chdir(str(root))

setup(
    name='eia',
    packages=find_packages(),
    version='0.1.0',
    description='Electronic Instrument Adapter SDK',
    author='Ariel Alvarez Windey, Gabriel Robles',
    author_email='ajalvarez@fi.uba.ar, grobles93@fi.uba.ar',
    install_requires=[],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==4.4.1'],
    # test_suite='tests',
)