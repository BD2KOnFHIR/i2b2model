
import datetime
import unittest
from collections import OrderedDict

from dynprops import heading, as_dict

from i2b2model.shared.i2b2core import I2B2Core


class OntologyTestCase(unittest.TestCase):
    def test_basics(self):
        from i2b2model.metadata.i2b2ontology import OntologyEntry
        from i2b2model.metadata.i2b2ontologyquery import ConceptQuery

        I2B2Core.download_date = datetime.datetime(2017, 5, 25)
        I2B2Core.sourcesystem_cd = "TEST"
        I2B2Core.import_date = datetime.datetime(2017, 5, 25)
        I2B2Core.update_date = datetime.datetime(2001, 12, 1)
        ontrec = OntologyEntry('\\X\\Y\\Z\\', ConceptQuery('\\X\\Y\\Z\\'), None, "17400008")
        self.assertEqual('c_hlevel\tc_fullname\tc_name\tc_synonym_cd\tc_visualattributes\t'
                         'c_totalnum\tc_basecode\tc_metadataxml\tc_facttablecolumn\tc_tablename\t'
                         'c_columnname\tc_columndatatype\tc_operator\tc_dimcode\tc_comment\t'
                         'c_tooltip\tm_applied_path\tupdate_date\tdownload_date\t'
                         'import_date\tsourcesystem_cd\tvaluetype_cd\tm_exclusion_cd\tc_path\tc_symbol',
                         heading(ontrec))
        # Note that hierarchy level is zero based
        self.assertEqual(OrderedDict([
             ('c_hlevel', 2),
             ('c_fullname', '\\X\\Y\\Z\\'),
             ('c_name', 'Z'),
             ('c_synonym_cd', 'N'),
             ('c_visualattributes', 'FAE'),
             ('c_totalnum', None),
             ('c_basecode', '17400008'),
             ('c_metadataxml', None),
             ('c_facttablecolumn', 'concept_cd'),
             ('c_tablename', 'concept_dimension'),
             ('c_columnname', 'concept_path'),
             ('c_columndatatype', 'T'),
             ('c_operator', '='),
             ('c_dimcode', '\\X\\Y\\Z\\'),
             ('c_comment', None),
             ('c_tooltip', None),
             ('m_applied_path', '@'),
             ('update_date', datetime.datetime(2001, 12, 1, 0, 0)),
             ('download_date', datetime.datetime(2017, 5, 25, 0, 0)),
             ('import_date', datetime.datetime(2017, 5, 25, 0, 0)),
             ('sourcesystem_cd', 'TEST'),
             ('valuetype_cd', None),
             ('m_exclusion_cd', None),
             ('c_path', None),
             ('c_symbol', None)]), as_dict(ontrec))


if __name__ == '__main__':
    unittest.main()
