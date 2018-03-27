
import unittest
from datetime import datetime, timedelta
from i2b2model.testingutils.base_test_case import BaseTestCase


class BaseTestCaseTestCase(BaseTestCase):
    def test_almostnow(self):
        self.assertTrue(self.almostnow(str(datetime.now())))
        self.assertTrue(self.almostnow(str(datetime.now() - timedelta(seconds=1))))
        self.assertFalse(self.almostnow(str(datetime.now() - timedelta(seconds=5))))

    def test_almostequal(self):
        self.assertTrue(self.almostequal(str(datetime.now()), str(datetime.now())))
        self.assertTrue(self.almostequal(str(datetime.now()), str(datetime.now() - timedelta(seconds=1))))
        self.assertFalse(self.almostequal(str(datetime.now()), str(datetime.now() - timedelta(seconds=5))))


if __name__ == '__main__':
    unittest.main()
