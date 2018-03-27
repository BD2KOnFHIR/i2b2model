import re
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from typing import Callable, List

import os

from i2b2model import __version__


class ScriptTestBase(unittest.TestCase):
    dirname = None
    save_output: bool = True              # Override this to save output
    tst_dir: str = None
    tst_fcn: Callable[[List[str]], bool] = None
    print_prefiltered = False

    @classmethod
    def call_tst_fcn(cls, args: str):
        return cls.tst_fcn(args.split())

    def check_output(self, test_file: str, output: str, multipart_test: bool=False) -> None:
        assert self.dirname is not None, "dirname must be set to local file path"
        fullfilename = os.path.join(self.dirname, 'data_out', self.tst_dir, test_file)
        if self.save_output:
            with open(fullfilename, 'w') as outf:
                outf.write(output)
        self.maxDiff = None
        with open(fullfilename) as testf:
            test_text = re.sub(r'Version: [0-9]+\.[0-9]+\.[[0-9]+', f'Version: {__version__}', testf.read(),
                               flags=re.MULTILINE)
            self.assertEqual(test_text, output)
        if not multipart_test:
            self.assertFalse(self.save_output, "save_output is true")

    def check_output_output(self, args: str,  test_file: str, exception: bool=False,
                            multipart_test: bool=False) -> None:
        output = StringIO()
        with redirect_stdout(output):
            if exception:
                with self.assertRaises(SystemExit):
                    self.call_tst_fcn(args)
            else:
                self.call_tst_fcn(args)
        self.check_output(test_file, output.getvalue(), multipart_test=multipart_test)

    def check_filtered_output(self, args: str, test_file: str, filtr: Callable[[str], str]) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.call_tst_fcn(args)
        if self.print_prefiltered:
            print(output.getvalue())
        self.check_output(test_file, filtr(output.getvalue()))

    def check_error_output(self, args: str, test_file: str, multipart_test: bool=False) -> None:
        output = StringIO()
        with redirect_stderr(output):
            with self.assertRaises(SystemExit):
                self.call_tst_fcn(args)
        self.check_output(test_file, output.getvalue(), multipart_test=multipart_test)
