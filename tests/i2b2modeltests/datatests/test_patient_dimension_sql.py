
import unittest
from datetime import datetime

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId, I2B2Core
from i2b2model.testingutils.connection_helper import connection_helper
from tests.utils.crc_testcase import CRCTestCase


class PatientDimensionSQLTestCase(CRCTestCase):
    opts = connection_helper(CRCTestCase.test_conf_file)

    def test_insert(self):
        from i2b2model.data.i2b2patientdimension import PatientDimension, VitalStatusCd

        I2B2Core.update_date = datetime(2017, 5, 25)

        with self.sourcesystem_cd():
            I2B2Core.sourcesystem_cd = self._sourcesystem_cd
            I2B2CoreWithUploadId.upload_id = self._upload_id

            # Add a brand new encounter mapping entry
            PatientDimension.delete_sourcesystem_cd(self.opts.tables, self._sourcesystem_cd)

            I2B2CoreWithUploadId.upload_id = self.opts.uploadid
            x = PatientDimension(12345)

            # Add a new patient dimension entry
            n_ins, n_upd = x.add_or_update_records(self.opts.tables, [x])
            self.assertEqual((0, 1), (n_upd, n_ins))

            # Make sure nothing happens when we re-enter it
            n_ins, n_upd = x.add_or_update_records(self.opts.tables, [x])
            self.assertEqual((0, 0), (n_upd, n_ins))

            # Change some properties on one and add another
            x.birth_date = datetime(2001, 12, 17)
            x.vital_status_cd = VitalStatusCd(VitalStatusCd.bd_day, VitalStatusCd.dd_living)
            y = PatientDimension(12346, VitalStatusCd(VitalStatusCd.bd_unknown, VitalStatusCd.dd_unknown))
            n_ins, n_upd = x.add_or_update_records(self.opts.tables, [x, y])
            self.assertEqual((1, 1), (n_upd, n_ins))
            self.assertEqual(2, x.delete_upload_id(self.opts.tables, x.upload_id))


if __name__ == '__main__':
    unittest.main()
