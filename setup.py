from setuptools import setup, find_packages

import sys

from i2b2model import __version__

requires = ['SQLAlchemy', 'psycopg2-binary', 'python-dateutil', 'dynprops']
if sys.version_info < (3, 5):
    requires.append('typing')
print(find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]))

setup(
    name='i2b2model',
    version=__version__,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    url='https://github.com/BD2KOnFHIR/i2b2model',
    license='Apache 2.0',
    author='Harold Solbrig',
    author_email='solbrig.harold@mayo.edu',
    description='i2b2 Model Wrapper',
    long_description='Representation of i2b2 model for Python based loading and manipulation',
    install_requires=requires,
    scripts=['scripts/removefacts', 'scripts/genconffile'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Database',
        'Programming Language :: Python :: 3.6'
    ]
)
