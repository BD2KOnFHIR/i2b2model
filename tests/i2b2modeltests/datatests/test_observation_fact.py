import unittest
from collections import OrderedDict
from datetime import datetime

from dynprops import heading, as_dict

from i2b2model.shared.i2b2core import I2B2Core
from tests.utils.crc_testcase import CRCTestCase


class ObservationFactTestCase(CRCTestCase):

    def test_basics(self):
        from i2b2model.data.i2b2observationfact import ObservationFact, ObservationFactKey
        I2B2Core.update_date = datetime(2017, 2, 19, 12, 33)
        with self.sourcesystem_cd():
            I2B2Core.sourcesystem_cd = self._sourcesystem_cd
            ofk = ObservationFactKey(12345, 23456, 'provider', datetime(2017, 5, 23, 11, 17))
            x = ObservationFact(ofk, 'fhir:concept')
            self.assertEqual('encounter_num\tpatient_num\tconcept_cd\tprovider_id\tstart_date\tmodifier_cd\t'
                             'instance_num\tvaltype_cd\ttval_char\tnval_num\tvalueflag_cd\tquantity_num\tunits_cd\t'
                             'end_date\tlocation_cd\tobservation_blob\tconfidence_num\tupdate_date\tdownload_date\t'
                             'import_date\tsourcesystem_cd\tupload_id', heading(x))
            self.assertEqual(OrderedDict([
                 ('encounter_num', 23456),
                 ('patient_num', 12345),
                 ('concept_cd', 'fhir:concept'),
                 ('provider_id', 'provider'),
                 ('start_date', datetime(2017, 5, 23, 11, 17)),
                 ('modifier_cd', '@'),
                 ('instance_num', 0),
                 ('valtype_cd', '@'),
                 ('tval_char', None),
                 ('nval_num', None),
                 ('valueflag_cd', None),
                 ('quantity_num', None),
                 ('units_cd', None),
                 ('end_date', None),
                 ('location_cd', None),
                 ('observation_blob', None),
                 ('confidence_num', None),
                 ('update_date', datetime(2017, 2, 19, 12, 33)),
                 ('download_date', datetime(2017, 2, 19, 12, 33)),
                 ('import_date', datetime(2017, 2, 19, 12, 33)),
                 ('sourcesystem_cd', self._sourcesystem_cd),
                 ('upload_id', None)]), as_dict(x))


if __name__ == '__main__':
    unittest.main()
