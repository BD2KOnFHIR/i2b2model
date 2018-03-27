
import unittest
from collections import OrderedDict
from datetime import datetime

from dynprops import heading, as_dict

from i2b2model.shared.tablenames import DEFAULT_ONTOLOGY_TABLE
from i2b2model.metadata.i2b2tableaccess import TableAccess


class TableAccessTestCase(unittest.TestCase):
    def setUp(self):
        TableAccess._clear()

    def defaultTestResult(self):
        TableAccess._clear()

    def test_fhir(self):
        TableAccess.c_entry_date = datetime(2018, 3, 24, 11, 12)
        ta = TableAccess('FHIR')
        self.assertEqual(('c_table_cd\tc_table_name\tc_protected_access\tc_hlevel\tc_fullname\tc_name\t'
                          'c_synonym_cd\tc_visualattributes\tc_totalnum\tc_basecode\tc_metadataxml\t'
                          'c_facttablecolumn\tc_dimtablename\tc_columnname\tc_columndatatype\tc_operator\t'
                          'c_dimcode\tc_comment\tc_tooltip\tc_entry_date\tc_change_date\tc_status_cd\t'
                          'valuetype_cd'), heading(ta))
        self.assertEqual(OrderedDict([
             ('c_table_cd', 'FHIR'),
             ('c_table_name', DEFAULT_ONTOLOGY_TABLE),
             ('c_protected_access', 'N'),
             ('c_hlevel', 1),
             ('c_fullname', '\\FHIR\\'),
             ('c_name', 'FHIR Resources'),
             ('c_synonym_cd', 'N'),
             ('c_visualattributes', 'CA '),
             ('c_totalnum', None),
             ('c_basecode', None),
             ('c_metadataxml', None),
             ('c_facttablecolumn', 'concept_cd'),
             ('c_dimtablename', 'concept_dimension'),
             ('c_columnname', 'concept_path'),
             ('c_columndatatype', 'T'),
             ('c_operator', '='),
             ('c_dimcode', '\\FHIR\\'),
             ('c_comment', None),
             ('c_tooltip', 'FHIR Resources'),
             ('c_entry_date', datetime(2018, 3, 24, 11, 12)),
             ('c_change_date', None),
             ('c_status_cd', None),
             ('valuetype_cd', None)]), as_dict(ta))

    def test_general(self):
        from i2b2model.metadata.i2b2ontologyquery import Query

        TableAccess.c_entry_date = datetime(2018, 3, 24, 11, 17)
        q = Query('ITCP_EVENTS', 'concept_cd', False, 'C_FULLNAME', '=', '\\SCT\\276746005')
        ta = TableAccess('SCT_ENV_EVENT', '\\SCT\\276746005\\', q, 2, 'Environmental event (event)')
        self.assertEqual(OrderedDict([
             ('c_table_cd', 'SCT_ENV_EVENT'),
             ('c_table_name', 'custom_meta'),
             ('c_protected_access', 'N'),
             ('c_hlevel', 2),
             ('c_fullname', '\\SCT\\276746005\\'),
             ('c_name', 'Environmental event (event)'),
             ('c_synonym_cd', 'N'),
             ('c_visualattributes', 'CA '),
             ('c_totalnum', None),
             ('c_basecode', None),
             ('c_metadataxml', None),
             ('c_facttablecolumn', 'concept_cd'),
             ('c_dimtablename', 'ITCP_EVENTS'),
             ('c_columnname', 'C_FULLNAME'),
             ('c_columndatatype', 'T'),
             ('c_operator', '='),
             ('c_dimcode', '\\SCT\\276746005'),
             ('c_comment', None),
             ('c_tooltip', 'Environmental event (event)'),
             ('c_entry_date', datetime(2018, 3, 24, 11, 17)),
             ('c_change_date', None),
             ('c_status_cd', None),
             ('valuetype_cd', None)]), as_dict(ta))


if __name__ == '__main__':
    unittest.main()
