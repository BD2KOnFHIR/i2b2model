import unittest
from collections import OrderedDict
from datetime import datetime

from dynprops import as_dict, heading

from i2b2model.shared.i2b2core import I2B2Core
from i2b2model.testingutils.base_test_case import BaseTestCase


class ConceptDimensionTestCase(BaseTestCase):
    def setUp(self):
        I2B2Core._clear()

    def tearDown(self):
        I2B2Core._clear()

    def test_basics(self):
        from i2b2model.metadata.i2b2conceptdimension import ConceptDimension

        ConceptDimension._clear()
        I2B2Core.download_date = datetime(2017, 5, 25)
        I2B2Core.sourcesystem_cd = "TEST_SS"
        I2B2Core.import_date = datetime(2017, 5, 25)

        cd = ConceptDimension('TEST', 'root', 'Root test concept', ['L1', 'L2', 'root'], '\\TEST\\')
        self.assertAlmostNow(cd.update_date)
        I2B2Core.update_date = datetime(2001, 12, 1)
        expected = OrderedDict([('concept_path', '\\TEST\\L1\\L2\\root\\'),
                                ('concept_cd', 'TEST:root'),
                                ('name_char', 'TEST Root test concept'),
                                ('concept_blob', ''),
                                ('update_date', datetime(2001, 12, 1, 0, 0)),
                                ('download_date', datetime(2017, 5, 25, 0, 0)),
                                ('import_date', datetime(2017, 5, 25, 0, 0)),
                                ('sourcesystem_cd', 'TEST_SS'),
                                ('upload_id', None)])
        self.assertEqual(expected, as_dict(cd))

        # Note - balance is actually a modifier.  This is strictly an example
        cd = ConceptDimension('TEST', 'root', 'Root balance test concept', ['L1', 'L2', 'balance'], '\\TEST\\')
        expected = OrderedDict([('concept_path', '\\TEST\\L1\\L2\\balance\\root\\'),
                                ('concept_cd', 'TEST:root'),
                                ('name_char', 'TEST Root balance test concept'),
                                ('concept_blob', ''),
                                ('update_date', datetime(2001, 12, 1, 0, 0)),
                                ('download_date', datetime(2017, 5, 25, 0, 0)),
                                ('import_date', datetime(2017, 5, 25, 0, 0)),
                                ('sourcesystem_cd', 'TEST_SS'),
                                ('upload_id', None)])
        self.assertEqual(expected, as_dict(cd))

    def test_interactions(self):
        """
        ModifierDimension and ConceptDimension share a common root.  If the dynelements lists are not specific to the
        subclasses, we end up with one composite
        """
        from i2b2model.metadata.i2b2conceptdimension import ConceptDimension
        from i2b2model.metadata.i2b2modifierdimension import ModifierDimension

        self.assertEqual('modifier_path\tmodifier_cd\tname_char\tmodifier_blob\tupdate_date\t'
                         'download_date\timport_date\tsourcesystem_cd\tupload_id', heading(ModifierDimension))
        self.assertEqual('concept_path\tconcept_cd\tname_char\tconcept_blob\tupdate_date\t'
                         'download_date\timport_date\tsourcesystem_cd\tupload_id', heading(ConceptDimension))


if __name__ == '__main__':
    unittest.main()
