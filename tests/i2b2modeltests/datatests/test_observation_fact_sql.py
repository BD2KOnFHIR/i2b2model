
import unittest
from datetime import datetime

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId, I2B2Core
from i2b2model.testingutils.connection_helper import connection_helper
from tests.utils.crc_testcase import CRCTestCase
from i2b2model.data.i2b2observationfact import ObservationFact


class ObservationFactSQLTestCase(CRCTestCase):
    opts = connection_helper(CRCTestCase.test_conf_file)

    def test_insert(self):
        from i2b2model.data.i2b2observationfact import ObservationFactKey

        print("{} records deleted".format(ObservationFact.delete_upload_id(self.opts.tables, self.opts.uploadid)))
        ofk = ObservationFactKey(12345, 23456, 'provider', datetime(2017, 5, 23, 11, 17))
        I2B2Core.update_date = datetime(2017, 2, 19, 12, 33)
        with self.sourcesystem_cd():
            I2B2CoreWithUploadId.upload_id = self.opts.uploadid
            I2B2Core.sourcesystem_cd = "FHIR R4"
            obsf = ObservationFact(ofk, 'fhir:concept')
            n_ins, n_upd = ObservationFact.add_or_update_records(self.opts.tables, [obsf])
            self.assertEqual((0, 1), (n_upd, n_ins))
            obsf.instance_num = 2
            I2B2Core.sourcesystem_cd = "FHIR R4z"
            obsf2 = ObservationFact(ofk, 'fhir:concept')
            obsf2.instance_num = 2
            obsf2.modifier_cd = "fhir:modifier"
            n_ins, n_upd = ObservationFact.add_or_update_records(self.opts.tables, [obsf, obsf2])
            self.assertEqual((0, 2), (n_upd, n_ins))
            self.assertEqual(3, ObservationFact.delete_upload_id(self.opts.tables, self.opts.uploadid))


if __name__ == '__main__':
    unittest.main()
