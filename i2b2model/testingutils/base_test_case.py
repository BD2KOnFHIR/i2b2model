import os
import unittest
from datetime import datetime, timedelta
from typing import Union

from dateutil.parser import parse


class BaseTestCase(unittest.TestCase):
    @staticmethod
    def almostnow(d: Union[datetime, str]) -> bool:
        if not isinstance(d, datetime):
            d = parse(d)
        return datetime.now() - d < timedelta(seconds=2)

    @staticmethod
    def almostequal(d1: Union[datetime, str], d2: Union[datetime, str]):
        if not isinstance(d1, datetime):
            d1 = parse(d1)
        if not isinstance(d2, datetime):
            d2 = parse(d2)
        return d1 - d2 < timedelta(seconds=2)

    def assertAlmostNow(self, d: Union[datetime, str]):
        self.assertTrue(self.almostnow(d))

    def assertDatesAlmostEqual(self, d1: str, d2: str):
        self.assertTrue(self.almostequal(d1, d2))


def make_and_clear_directory(dirbase: str):
    import shutil
    safety_file = os.path.join(dirbase, "generated")
    if os.path.exists(dirbase):
        if not os.path.exists(safety_file):
            raise FileExistsError("{} not found in test directory".format(safety_file))
        shutil.rmtree(dirbase)
    os.makedirs(dirbase)
    with open(os.path.join(dirbase, "generated"), "w") as f:
        f.write("Generated for safety.  Must be present for test to remove this directory.")
