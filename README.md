# i2b2model
Python tools for working with the i2b2 data model


[![PyPi](https://version-image.appspot.com/pypi/?name=i2b2model)](https://pypi.python.org/pypi/i2b2model)

[![Pyversions](https://img.shields.io/pypi/pyversions/i2b2model.svg)](https://pypi.python.org/pypi/i2b2model)

## Edit history
* 0.1.0 - Initial commit.  Parted from the [i2FHIRb2](https://github.com/BD2KONFHIR/i2FHIRb2/) module
* 0.1.1 - Added hlevel bias and ability to explicitly set c_name in OntologyEntry
* 0.1.2 - Added more options to TableAccess to support i2b2terminology project
* 0.1.3 - Moved OntologyRoot from i2FHIRb2 to here
* 0.2.0 - Refactored for dynprops

## Requirements
1) Python 3.6 or later
2) Instance of the [i2b2](https://www.i2b2.org/) database - version 1.7 or later.  _Note_: this has only been tested on the postgres version of i2b2.

## Installation
Installing the current version:
```text
> pip install i2b2model
```

To install the absolute latest:
```text
> pip install git+https://github.com/BD2KONFHIR/i2b2model
```

## Setup

1) Select a working directory and create a configuration file:
```text
> genconffile
db_conf generated
```

2) Edit the configuration file and add the appropriate parameters.  
```text
> cat db_conf
-db postgresql+psycopg2://localhost:5432/i2b2
--user i2b2
--password demouser
```

See the [removefacts help file](scripts/removefacts.md) for details
