import io
import sys
import unittest
from contextlib import contextmanager, redirect_stdout
from functools import reduce

from i2b2model.scripts.removefacts import remove_facts
from i2b2model.shared.i2b2core import I2B2Core, I2B2CoreWithUploadId
from dynprops import clear


class CRCTestCaseBase(unittest.TestCase):
    test_prefix = None
    test_conf_file = None

    def setUp(self):
        self.assertIsNotNone(self.test_prefix, "CRCTestCase.test_prefix must be set")
        self.assertIsNotNone(self.test_conf_file, "CRCTestCase.test_conf_file location must be set")
        clear(I2B2Core)
        clear(I2B2CoreWithUploadId)

    def tearDown(self):
        # if getattr(self, "_sourcesystem_cd", None):
        #     remove_facts(f"--conf {self.test_conf_file} -ss {self._sourcesystem_cd}".split())
        clear(I2B2Core)
        clear(I2B2CoreWithUploadId)

    @staticmethod
    def text_to_number(txt: str) -> int:
        return reduce(lambda acc, upd: (((acc ^ ord(upd)) << 8) + ord(upd)) % 0xFFFF, txt, sys.maxsize)

    @contextmanager
    def sourcesystem_cd(self) -> str:
        """ Generate a sourcesystem_code that identifies the test case and make sure it doesn't pollute the database.
        _sourcesystem_cd and _upload_id are added to the specific object

        :return: sourcesystem code
        """
        save_ss_cd = getattr(self, "_sourcesystem_cd", None)
        save_up_id = getattr(self, "_upload_id", None)
        self._sourcesystem_cd = self.test_prefix + type(self).__name__
        self._upload_id = self.text_to_number(self._sourcesystem_cd)
        try:
            yield self._sourcesystem_cd
        finally:
            debug_output = io.StringIO()
            with redirect_stdout(debug_output):
                remove_facts(f"--conf {self.test_conf_file} -ss {self._sourcesystem_cd}".split())
                print(f"      {self._upload_id}")
                print(f"----- {self._sourcesystem_cd}")
            # print(debug_output.getvalue())
            if save_ss_cd:
                self._sourcesystem_cd = save_ss_cd
                self._upload_id = save_up_id
            else:
                delattr(self, '_sourcesystem_cd')
                delattr(self, '_upload_id')
