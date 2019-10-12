"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="simulacion2019",
    version="1.0.0",
    description="Programa para la Cátedra de Simulación 2019 UTN FRC",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/agusventuri/simulacion2019",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: GNU",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["ui", "models"],
    include_package_data=True,
    install_requires=[
        'cycler',
        'kiwisolver',
        'matplotlib',
        'numpy',
        'pandas',
        'pyparsing',
        'python-dateutil',
        'pytz',
        'six'
    ],
    entry_points={"console_scripts": ["generador=ui.__main__:main"]},
)
