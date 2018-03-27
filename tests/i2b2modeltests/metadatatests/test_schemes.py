
import unittest

from dynprops import as_dict, heading, row, OrderedDict

from i2b2model.metadata.i2b2schemes import Schemes
from i2b2model.testingutils.connection_helper import connection_helper
from tests.utils.crc_testcase import CRCTestCase


class SchemesTestcase(unittest.TestCase):
    opts = connection_helper(CRCTestCase.test_conf_file)
    rec = Schemes("TestCodeSystem", "A test coding system", "Used for unit tests - you should never see this")

    def setUp(self):
        self.rec.del_record(self.opts.tables)

    def tearDown(self):
        self.rec.del_record(self.opts.tables)

    def test_create(self):
        self.assertEqual("c_key\tc_name\tc_description", heading(self.rec))
        self.assertEqual('TestCodeSystem\tA test coding system\tUsed for unit tests - you should never see this',
                         row(self.rec))
        self.assertEqual(OrderedDict([
             ('c_key', 'TestCodeSystem'),
             ('c_name', 'A test coding system'),
             ('c_description',
              'Used for unit tests - you should never see this')]), as_dict(self.rec))

        self.assertEqual((1, 0), self.rec.add_or_update_record(self.opts.tables))
        self.assertEqual((0, 0), self.rec.add_or_update_record(self.opts.tables))
        self.rec.c_description = "Used for tests"
        self.assertEqual((0, 1), self.rec.add_or_update_record(self.opts.tables))
        self.assertEqual(1, self.rec.del_record(self.opts.tables))
        self.assertEqual(0, self.rec.del_record(self.opts.tables))


if __name__ == '__main__':
    unittest.main()
