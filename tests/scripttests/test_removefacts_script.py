
import unittest

import os

from i2b2model import __version__
from i2b2model.scripts.removefacts import remove_facts
from i2b2model.testingutils.script_test_base import ScriptTestBase
from tests.utils.crc_testcase import CRCTestCase


class RemoveFactsTestCase(ScriptTestBase):
    ScriptTestBase.dirname = os.path.abspath(os.path.dirname(__file__))
    ScriptTestBase.version = __version__

    @classmethod
    def setUpClass(cls):
        cls.dirname = os.path.split(os.path.abspath(__file__))[0]
        cls.save_output = False
        cls.tst_dir = "removefacts"
        cls.tst_fcn = remove_facts

    def test_no_args(self):
        self.check_error_output("", "noargs")

    def test_help(self):
        self.check_output_output("-h", "help", exception=True)

    def test_no_config_file(self):
        self.check_error_output("-u 12345", "noconfig")

    def test_onearg(self):
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} -u 123450 -u 123450", "onearg")

    def test_threeargs(self):
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} -u 123450 123460 123470", "threeargs")

    def test_sourcesystem(self):
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} --sourcesystem SAMPLE", "sourcesystem")

    def test_ss_and_id(self):
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} -u 123450 -ss SAMPLE", "ssandid")

    def test_config_parms(self):
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} -u 123450", "confparms")

    def test_list_testlist(self):
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} --testlist", "testlist1", multipart_test=True)
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} -p TEST_ITEM_ --testlist", "testlist2")

    def test_remove_testlist(self):
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} --removetestlist", "removelist1",
                                 multipart_test=True)
        self.check_output_output(f"--conf {CRCTestCase.test_conf_file} -p TEST_ITEM_ --removetestlist", "removelist2")

    def test_remove_and_ss(self):
        self.check_error_output(f"--conf {CRCTestCase.test_conf_file} --removetestlist -ss X", "removeerror1",
                                multipart_test=True)
        self.check_error_output(f"--conf {CRCTestCase.test_conf_file} -p TEST_ITEM_ --removetestlist -u 1",
                                "removeerror2")


if __name__ == '__main__':
    unittest.main()
