
import unittest


class DimensionQueryTestCase(unittest.TestCase):

    def test_concept_query(self):
        from i2b2model.metadata.i2b2ontologyquery import ConceptQuery
        from i2b2model.metadata.i2b2ontology import OntologyEntry

        q = ConceptQuery("foo")
        self.assertEqual("SELECT concept_cd\nFROM concept_dimension\nWHERE concept_path = 'foo'", str(q))
        q.where_obj = '\\path\\%'
        self.assertEqual("SELECT concept_cd\nFROM concept_dimension\nWHERE concept_path = '\\path\\%'", str(q))
        o = OntologyEntry("\\PATH\\subpath\\", ConceptQuery('\\PATH\\subpath\\'), None, "74400008")
        self.assertEqual(o.c_facttablecolumn, 'concept_cd')
        self.assertEqual(o.c_tablename, 'concept_dimension')
        self.assertEqual(o.c_columndatatype, 'T')
        self.assertEqual(o.c_columnname, 'concept_path')
        self.assertEqual(o.c_operator, '=')
        self.assertEqual(o.c_dimcode, '\\PATH\\subpath\\')

    def test_empty_query(self):
        from i2b2model.metadata.i2b2ontologyquery import EmptyQuery
        from i2b2model.metadata.i2b2ontology import OntologyEntry

        q = EmptyQuery()
        self.assertEqual("NO QUERY", str(q))
        o = OntologyEntry("\\PATH\\subpath\\", EmptyQuery(), None, "74400008")
        self.assertEqual(o.c_facttablecolumn, '')
        self.assertEqual(o.c_tablename, '')
        self.assertEqual(o.c_columndatatype, 'T')
        self.assertEqual(o.c_columnname, '')
        self.assertEqual(o.c_operator, '')
        self.assertEqual(o.c_dimcode, '')

    def test_modifier_query(self):
        from i2b2model.metadata.i2b2ontologyquery import ModifierQuery
        from i2b2model.metadata.i2b2ontology import OntologyEntry

        q = ModifierQuery("foo")
        self.assertEqual("SELECT modifier_cd\nFROM modifier_dimension\nWHERE modifier_path like 'foo'", str(q))
        o = OntologyEntry("\\PATH\\subpath\\", ModifierQuery('\\PATH\\subpath\\'), None, "74400008")
        self.assertEqual(o.c_facttablecolumn, 'modifier_cd')
        self.assertEqual(o.c_tablename, 'modifier_dimension')
        self.assertEqual(o.c_columndatatype, 'T')
        self.assertEqual(o.c_columnname, 'modifier_path')
        self.assertEqual(o.c_operator, 'like')
        self.assertEqual(o.c_dimcode, '\\PATH\\subpath\\')

    def test_patient_query(self):
        from i2b2model.metadata.i2b2ontologyquery import PatientQuery
        from i2b2model.metadata.i2b2ontology import OntologyEntry

        q = PatientQuery('patient_num', '=', 12345)
        self.assertEqual("SELECT patient_num\nFROM patient_dimension\nWHERE patient_num = 12345", str(q))
        pq = PatientQuery(
            'birth_date',
            'BETWEEN',
            "(CURRENT_DATE - INTERVAL '731.5 day') AND"
            " (CURRENT_DATE - INTERVAL '366.25 day')")
        self.assertEqual("SELECT patient_num\nFROM patient_dimension\n"
                         "WHERE birth_date BETWEEN "
                         "(CURRENT_DATE - INTERVAL '731.5 day') AND "
                         "(CURRENT_DATE - INTERVAL '366.25 day')", str(pq))
        o = OntologyEntry("\\PATH\\subpath\\", pq, None, "Q117.3")
        self.assertEqual(o.c_facttablecolumn, 'patient_num')
        self.assertEqual(o.c_tablename, 'patient_dimension')
        self.assertEqual(o.c_columndatatype, 'N')
        self.assertEqual(o.c_columnname, 'birth_date')
        self.assertEqual(o.c_operator, 'BETWEEN')
        self.assertEqual(o.c_dimcode, "(CURRENT_DATE - INTERVAL '731.5 day') "
                                      "AND (CURRENT_DATE - INTERVAL '366.25 day')")

    def test_visit_query(self):
        from i2b2model.metadata.i2b2ontologyquery import VisitQuery
        from i2b2model.metadata.i2b2ontology import OntologyEntry

        vq = VisitQuery('length_of_stay', '>', 10)
        self.assertEqual("SELECT encounter_num\nFROM visit_dimension\nWHERE length_of_stay > 10", str(vq))
        o = OntologyEntry("\\PATH\\subpath\\", vq, None, "Q117.3")
        self.assertEqual(o.c_facttablecolumn, 'encounter_num')
        self.assertEqual(o.c_tablename, 'visit_dimension')
        self.assertEqual(o.c_columndatatype, 'N')
        self.assertEqual(o.c_columnname, 'length_of_stay')
        self.assertEqual(o.c_operator, '>')
        self.assertEqual(o.c_dimcode, 10)


if __name__ == '__main__':
    unittest.main()
