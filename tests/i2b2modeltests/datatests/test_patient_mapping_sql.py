
import unittest

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId
from i2b2model.testingutils.connection_helper import connection_helper
from tests.utils.crc_testcase import CRCTestCase


class PatientMappingSQLTestCase(unittest.TestCase):
    opts = connection_helper(CRCTestCase.test_conf_file)

    def test_insert(self):
        from i2b2model.data.i2b2patientmapping import PatientMapping, PatientIDEStatus

        PatientMapping.delete_upload_id(self.opts.tables, self.opts.uploadid)
        I2B2CoreWithUploadId.upload_id = self.opts.uploadid
        pm = PatientMapping(10000001, "12345", PatientIDEStatus.active, "http://hl7.org/fhir/", "fhir")

        n_ins, n_upd = PatientMapping.add_or_update_records(self.opts.tables, [pm])
        self.assertEqual((0, 1), (n_upd, n_ins))
        n_ins, n_upd = PatientMapping.add_or_update_records(self.opts.tables, [pm])
        self.assertEqual((0, 0), (n_upd, n_ins))
        pm.project_id = "TEST"

        pm2 = PatientMapping(10000001, "12346", PatientIDEStatus.active, "http://hl7.org/fhir/", "fhir")
        n_ins, n_upd = PatientMapping.add_or_update_records(self.opts.tables, [pm, pm2])
        self.assertEqual((0, 2), (n_upd, n_ins))
        self.assertEqual(3, PatientMapping.delete_upload_id(self.opts.tables, self.opts.uploadid))


if __name__ == '__main__':
    unittest.main()
