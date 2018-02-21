# `removefacts` 
`removefacts` is a command line utility for removing i2b2 observation facts that are associated with one or more upload identifiers.

## Usage:
```text
usage: removefacts [-h] [-ss SOURCE SYSTEM CODE]
                   [-u [UPLOAD IDENTIFIER [UPLOAD IDENTIFIER ...]]]
                   [--conf CONFIG FILE] [-db DBURL] [--user USER]
                   [--password PASSWORD] [--crcdb CRCDB] [--crcuser CRCUSER]
                   [--crcpassword CRCPASSWORD] [--ontodb ONTODB]
                   [--ontouser ONTOUSER] [--ontopassword ONTOPASSWORD]
                   [--onttable ONTOLOGY TABLE NAME] [-p SS PREFIX]
                   [--testlist] [--removetestlist]

Clear data from FHIR observation fact table

optional arguments:
  -h, --help            show this help message and exit
  -ss SOURCE SYSTEM CODE, --sourcesystem SOURCE SYSTEM CODE
                        Sourcesystem code
  -u [UPLOAD IDENTIFIER [UPLOAD IDENTIFIER ...]], --uploadid [UPLOAD IDENTIFIER [UPLOAD IDENTIFIER ...]]
                        Upload identifer -- uniquely identifies this batch
  --conf CONFIG FILE    Configuration file
  -db DBURL, --dburl DBURL
                        Default database URL
  --user USER           Default user name
  --password PASSWORD   Default password
  --crcdb CRCDB         CRC database URL. (default: dburl)
  --crcuser CRCUSER     User name for CRC database. (default: user)
  --crcpassword CRCPASSWORD
                        Password for CRC database. (default: password)
  --ontodb ONTODB       Ontology database URL. (default: dburl)
  --ontouser ONTOUSER   User name for ontology database. (default: user)
  --ontopassword ONTOPASSWORD
                        Password for ontology database. (default: password)
  --onttable ONTOLOGY TABLE NAME
                        Ontology table name (default: custom_meta)
  -p SS PREFIX, --testprefix SS PREFIX
                        Sourcesystem_cd prefix for test suite functions
                        (Default: test_i2b2model_
  --testlist            List leftover test suite entries
  --removetestlist      Remove leftover test suite entries
```

## Example
Suppose that you've done two different loads:

```text
> loadfacts --conf db_conf -l -u 17134
> loadfacts --conf db_conf -l -u 17135
```
To undo the results of this load process.


```text
> removefacts --conf db_conf 17134 17135
```

Similarly, suppose you have loaded a large batch of test data:

```text
> loadfacts --conf db_conf -l -u 17134 -ss BATCH_LOAD
```

To undo this:
```text
> removefacts --conf db_conf -ss BATCH_LOAD
```

You can also use subsystem_cd prefixes for testing and other work:

```text
> loadfacts --conf db_conf -l -ss TEST_BATCH_1
> loadfacts --conf db_conf -l -ss TEST_BATCH_2
```

```text
> removefacts --conf db_conf -ss TEST_BATCH_ --testlist
---> Listing orphan test elements for sourcesystem_cd starting with TEST_BATCH_
TABLE: TEST_BATCH_1 	: i2b2demodata.patient_dimension
TABLE: TEST_BATCH_1 	: i2b2demodata.patient_mapping
TABLE: TEST_BATCH_1 	: i2b2demodata.visit_dimension
TABLE: TEST_BATCH_1 	: i2b2demodata.encounter_mapping
TABLE: TEST_BATCH_1 	: i2b2demodata.observation_fact
TABLE: TEST_BATCH_2 	: i2b2demodata.observation_fact

> removefacts --conf db_conf -ss TEST_BATCH_ --removetestlist
---> Removing orphan test elements for sourcesystem_cd starting with TEST_BATCH_
TABLE: TEST_BATCH_1 	: i2b2demodata.patient_dimension
TABLE: TEST_BATCH_1 	: i2b2demodata.patient_mapping
TABLE: TEST_BATCH_1 	: i2b2demodata.visit_dimension
TABLE: TEST_BATCH_1 	: i2b2demodata.encounter_mapping
TABLE: TEST_BATCH_1 	: i2b2demodata.observation_fact
TABLE: TEST_BATCH_2 	: i2b2demodata.observation_fact
1 rows removed from i2b2demodata.visit_dimension
1 rows removed from i2b2demodata.encounter_mapping
        ...
```
