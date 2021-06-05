# Example for creating a python lib:
# https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

from setuptools import find_packages, setup

setup(
    name='electronic-instrument-adapter-sdk',
    packages=find_packages(include=['electronic-instrument-adapter-sdk']),
    version='0.1.0',
    description='Electronic Instrument Adapter SDK',
    author='Ariel Alvarez Windey, Gabriel Robles',
    author_email='ajalvarez@fi.uba.ar, grobles93@fi.uba.ar',
    install_requires=[],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==4.4.1'],
    # test_suite='tests',
)