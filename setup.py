from os import path
from setuptools import setup, find_packages

from i2b2model import __version__

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    long_description = f.read()

packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
packages.extend(['tests.scripts', 'tests.utils'])

setup(
    name='i2b2model',
    version=__version__,
    description='i2b2 Model Wrapper',
    long_description=long_description,
    url='https://github.com/BD2KOnFHIR/i2b2model',
    license='Apache 2.0',
    author='Harold Solbrig',
    author_email='solbrig.harold@mayo.edu',
    packages=packages,
    package_data={'tests.utils': ['db_conf']},
    install_requires=['SQLAlchemy', 'psycopg2-binary', 'python-dateutil', 'dynprops'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Database',
        'Programming Language :: Python :: 3.6'
    ]
)
