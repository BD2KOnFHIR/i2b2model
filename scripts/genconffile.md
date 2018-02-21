# `genconffile` 
`genconffile` creates a default database configuration file so you don't have to look for a template

## Usage:
```text
usage: genconffile [-h] [-f Config File]

Generate SQL db_conf file template

optional arguments:
  -h, --help            show this help message and exit
  -f Config File, --configfile Config File
                        File name to generate (Default: db_conf)
```

```text
> genconffile
db_conf generated
> cat db_conf
-db postgresql+psycopg2://localhost:5432/i2b2
--user i2b2
--password demouser

>
```