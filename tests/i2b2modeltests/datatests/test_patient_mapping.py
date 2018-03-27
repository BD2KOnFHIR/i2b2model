
import unittest
from collections import OrderedDict
from datetime import datetime

from dynprops import as_dict

from i2b2model.shared.i2b2core import I2B2Core, I2B2CoreWithUploadId
from tests.utils.crc_testcase import CRCTestCase


class PatientMappingTestCase(CRCTestCase):
    def test_patient_mapping(self):
        from i2b2model.data.i2b2patientmapping import PatientMapping
        from i2b2model.data.i2b2patientmapping import PatientIDEStatus

        I2B2Core.update_date = datetime(2017, 5, 25)
        with self.sourcesystem_cd():
            I2B2Core.sourcesystem_cd = self._sourcesystem_cd
            pm = PatientMapping(10000001, "p123", PatientIDEStatus.active, "http://hl7.org/fhir/", "fhir")
            I2B2CoreWithUploadId.upload_id = 17443

            self.assertEqual(OrderedDict([
                 ('patient_ide', 'p123'),
                 ('patient_ide_source', 'http://hl7.org/fhir/'),
                 ('patient_num', 10000001),
                 ('patient_ide_status', 'A'),
                 ('project_id', 'fhir'),
                 ('update_date', datetime(2017, 5, 25, 0, 0)),
                 ('download_date', datetime(2017, 5, 25, 0, 0)),
                 ('import_date', datetime(2017, 5, 25, 0, 0)),
                 ('sourcesystem_cd', self._sourcesystem_cd),
                 ('upload_id', 17443)]), as_dict(pm))


if __name__ == '__main__':
    unittest.main()
