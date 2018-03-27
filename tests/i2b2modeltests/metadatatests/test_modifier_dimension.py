import unittest
from collections import OrderedDict
from datetime import datetime

from dynprops import as_dict

from i2b2model.shared.i2b2core import I2B2Core
from i2b2model.testingutils.base_test_case import BaseTestCase


class ModifierDimensionTestCase(BaseTestCase):
    def setUp(self):
        I2B2Core._clear()

    def tearDown(self):
        I2B2Core._clear()

    def test_basics(self):
        from i2b2model.metadata.i2b2modifierdimension import ModifierDimension

        I2B2Core.download_date = datetime(2017, 5, 25)
        I2B2Core.sourcesystem_cd = "MOD_TEST"
        I2B2Core.import_date = datetime(2017, 5, 25)
        md = ModifierDimension('MODTEST', 'baboon', 'Wild baboons', ['Earth', 'Africa', 'Zimbabwai'])
        self.assertAlmostNow(md.update_date)
        I2B2Core.update_date = datetime(2001, 12, 1)
        expected = OrderedDict([
             ('modifier_path', '\\Earth\\Africa\\Zimbabwai\\baboon\\'),
             ('modifier_cd', 'MODTEST:baboon'),
             ('name_char', 'MODTEST Wild baboons'),
             ('modifier_blob', ''),
             ('update_date', datetime(2001, 12, 1, 0, 0)),
             ('download_date', datetime(2017, 5, 25, 0, 0)),
             ('import_date', datetime(2017, 5, 25, 0, 0)),
             ('sourcesystem_cd', 'MOD_TEST'),
             ('upload_id', None)])
        self.assertEqual(expected, as_dict(md))


if __name__ == '__main__':
    unittest.main()
