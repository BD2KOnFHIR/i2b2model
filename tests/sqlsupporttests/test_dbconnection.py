import os
import unittest

from i2b2model.sqlsupport.dbconnection import process_parsed_args
from i2b2model.sqlsupport.file_aware_parser import FileAwareParser


class DBConnectionTestCase(unittest.TestCase):
    conf_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

    def test_decodefileargs1(self):
        from i2b2model.sqlsupport.dbconnection import add_connection_args

        parser = FileAwareParser()
        parser.add_argument('-mv', '--metadatavoc', help="Unused")
        add_connection_args(parser)
        opts = parser.parse_args(parser.decode_file_args(f"--conf {os.path.join(self.conf_dir, 'db_conf')}".split()))
        self.assertEqual("postgresql+psycopg2://localhost:5432/i2b2", opts.crcdb)
        self.assertEqual("postgresql+psycopg2://localhost:5433/i2b2", opts.ontodb)
        self.assertEqual("postgresql+psycopg2://localhost:5431/i2b2", opts.dburl)
        self.assertEqual('../tests/data/fhir_metadata_vocabulary', opts.metadatavoc)
        self.assertEqual('postgres', opts.user)
        self.assertEqual('postgres', opts.password)

    def test_decodefileargs2(self):
        from i2b2model.sqlsupport.dbconnection import add_connection_args

        parser = FileAwareParser()
        add_connection_args(parser)
        opts = process_parsed_args(
            parser.parse_args(
                parser.decode_file_args("--conf {}".format(os.path.join(self.conf_dir, 'db_conf_2')).split())),
            None, False)
        self.assertEqual("postgresql+psycopg2://localhost:5431/i2b2", opts.crcdb)
        self.assertEqual("user2", opts.crcuser)
        self.assertEqual("password1", opts.crcpassword)
        self.assertEqual("postgresql+psycopg2://localhost:5433/i2b2", opts.ontodb)
        self.assertEqual("postgresql+psycopg2://localhost:5431/i2b2", opts.dburl)
        self.assertEqual('user1', opts.ontouser)
        self.assertEqual('password1', opts.ontopassword)


if __name__ == '__main__':
    unittest.main()
