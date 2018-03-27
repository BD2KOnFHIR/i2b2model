
import unittest
from argparse import Namespace

from i2b2model.scripts.removefacts import list_test_artifacts
from i2b2model.testingutils.connection_helper import connection_helper
from tests.utils.crc_testcase import CRCTestCase


class CRCTestCaseTestCase(CRCTestCase):

    def test_clean_exit(self):
        """ Determine whether the test cases all cleaned up after themselves """
        ch = connection_helper(CRCTestCase.test_conf_file)
        opts = Namespace()
        opts.testprefix = CRCTestCase.test_prefix
        qr = list_test_artifacts(opts, ch.tables)
        self.assertFalse(bool(qr), """Run 'removefacts --conf <config> --removetestlist' or 
execute 'tests/utils/removetestfacts.py' to fix""")

    def test_sourcesystem_cd(self):
        """ Test CRCTestCase.sourcesystem_cd() nesting """
        with self.sourcesystem_cd():
            self.assertEqual(CRCTestCase.test_prefix + type(self).__name__, self._sourcesystem_cd)
            with self.sourcesystem_cd():
                self.assertEqual(CRCTestCase.test_prefix + type(self).__name__, self._sourcesystem_cd)
        self.assertIsNone(getattr(self, "_sourcesystem_cd", None))
        self.assertIsNone(getattr(self, "_upload_id", None))

    @unittest.expectedFailure
    def test_sourcesystem_cd_2(self):
        """ Test CRCTestCase.sourcesystem_cd() assertion failure processing """
        with self.sourcesystem_cd():
            self.assertEqual(CRCTestCase.test_prefix + type(self).__name__, self._sourcesystem_cd)
            self.assertEqual(117651, self._upload_id, "This should fail with '117651 != 13735'")
            self.assertTrue(False)

    def test_zsourcesystem_cd(self):
        """ Second half of ``test_sourcesystem_cd_2`` test """
        self.assertIsNone(getattr(self, "_sourcesystem_cd", None))


if __name__ == '__main__':
    unittest.main()
