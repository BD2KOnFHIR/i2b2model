import unittest

from sqlalchemy import select

from i2b2model.sqlsupport.dbconnection import process_parsed_args, add_connection_args
from i2b2model.sqlsupport.file_aware_parser import FileAwareParser
from tests.utils.crc_testcase import CRCTestCase


def caught_error(message):
    raise ValueError(message)  # reraise an error


# NOTE: if you get a "no tests" error, it is because parse_args does an exit(1).  Chances are
# the issue is in the location of the db_conf file
class I2B2TablesTestCase(unittest.TestCase):
    parser = FileAwareParser()
    add_connection_args(parser, strong_config_file=False)
    opts = parser.parse_args(f"--conf {CRCTestCase.test_conf_file}".split())
    process_parsed_args(opts, None)

    def test_basics(self):
        from i2b2model.sqlsupport.dbconnection import I2B2Tables
        x = I2B2Tables(self.opts)

        self.assertEqual(['concept_path',
                          'concept_cd',
                          'name_char',
                          'concept_blob',
                          'update_date',
                          'download_date',
                          'import_date',
                          'sourcesystem_cd',
                          'upload_id'], x.concept_dimension.columns.keys())
        s = select([x.ontology_table]).order_by(x.ontology_table.c.c_hlevel).limit(10)

        for e in x.crc_engine.execute(s).fetchall():
            self.assertTrue(e[0] < 2)

    def test_as_dict(self):
        from i2b2model.sqlsupport.dbconnection import I2B2Tables
        x = I2B2Tables(self.opts)

        self.assertEqual(x.concept_dimension, x['concept_dimension'])
        self.assertEqual('custom_meta', x['ontology_table'].name)


if __name__ == '__main__':
    unittest.main()
