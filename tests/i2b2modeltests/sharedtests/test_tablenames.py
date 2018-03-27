
import unittest


class TableNamesTestCase(unittest.TestCase):
    def test(self):
        from i2b2model.shared.tablenames import i2b2tablenames
        self.assertEqual("concept_dimension", i2b2tablenames.concept_dimension)
        self.assertEqual("ontology_table", i2b2tablenames.ontology_table)
        self.assertEqual("custom_meta", i2b2tablenames.phys_name(i2b2tablenames.ontology_table))
        self.assertEqual("concept_dimension", i2b2tablenames.phys_name(i2b2tablenames.concept_dimension))
        with self.assertRaises(AttributeError):
            _ = i2b2tablenames.other_dimension
        with self.assertRaises(KeyError):
            _ = i2b2tablenames.phys_name("foo")
        self.assertEqual([
             'concept_dimension',
             'encounter_mapping',
             'modifier_dimension',
             'observation_fact',
             'ontology_table',
             'patient_dimension',
             'patient_mapping',
             'provider_dimension',
             'schemes',
             'table_access',
             'visit_dimension'], i2b2tablenames.all_tables())

        i2b2tablenames.ontology_table = "another_ontology_table"
        self.assertEqual("ontology_table", i2b2tablenames.ontology_table)
        self.assertEqual("another_ontology_table", i2b2tablenames.phys_name(i2b2tablenames.ontology_table))
        i2b2tablenames._clear()
        self.assertEqual("concept_dimension", i2b2tablenames.concept_dimension)
        self.assertEqual("ontology_table", i2b2tablenames.ontology_table)
        self.assertEqual("custom_meta", i2b2tablenames.phys_name(i2b2tablenames.ontology_table))
        self.assertEqual("concept_dimension", i2b2tablenames.phys_name(i2b2tablenames.concept_dimension))


if __name__ == '__main__':
    unittest.main()
