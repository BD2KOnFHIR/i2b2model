
import unittest
from datetime import datetime

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId
from i2b2model.testingutils.connection_helper import connection_helper
from tests.utils.crc_testcase import CRCTestCase


class VisitDimensionSQLTestCase(unittest.TestCase):
    opts = connection_helper(CRCTestCase.test_conf_file)

    def test_insert(self):
        from i2b2model.data.i2b2visitdimension import VisitDimension, ActiveStatusCd

        VisitDimension.delete_upload_id(self.opts.tables, self.opts.uploadid)
        I2B2CoreWithUploadId.upload_id = self.opts.uploadid

        x = VisitDimension(5000017, 10000017, ActiveStatusCd(ActiveStatusCd.sd_day, ActiveStatusCd.ed_year),
                           datetime(2007, 12, 9), datetime(2008, 1, 1))

        n_ins, n_upd = x.add_or_update_records(self.opts.tables, [x])
        self.assertEqual((0, 1), (n_upd, n_ins))
        n_ins, n_upd = x.add_or_update_records(self.opts.tables, [x])
        self.assertEqual((0, 0), (n_upd, n_ins))
        x.end_date = datetime(2010, 2, 1)
        x.active_status_cd_.endcode = ActiveStatusCd.ed_month
        y = VisitDimension(5000018, 10000017, ActiveStatusCd(ActiveStatusCd.sd_day, ActiveStatusCd.ed_year),
                           datetime(2007, 12, 9), datetime(2008, 1, 1))

        n_ins, n_upd = x.add_or_update_records(self.opts.tables, [x, y])
        self.assertEqual((1, 1), (n_upd, n_ins))
        self.assertEqual(2, x.delete_upload_id(self.opts.tables, x.upload_id))


if __name__ == '__main__':
    unittest.main()
