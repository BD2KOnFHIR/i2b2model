
import unittest
from collections import OrderedDict
from datetime import datetime

from dynprops import as_dict

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId, I2B2Core
from tests.utils.crc_testcase import CRCTestCase


class VisitDimensionTestCase(CRCTestCase):

    def test_basics(self):
        from i2b2model.data.i2b2visitdimension import VisitDimension, ActiveStatusCd

        I2B2Core.update_date = datetime(2017, 1, 3)
        with self.sourcesystem_cd():
            I2B2CoreWithUploadId.upload_id = self._upload_id
            I2B2Core.sourcesystem_cd = self._sourcesystem_cd
            x = VisitDimension(500001, 10000017, ActiveStatusCd(ActiveStatusCd.sd_day,
                                                                ActiveStatusCd.ed_ongoing), datetime(2007, 10, 4))
            self.assertEqual(OrderedDict([
                 ('encounter_num', 500001),
                 ('patient_num', 10000017),
                 ('active_status_cd', 'OD'),
                 ('start_date', datetime(2007, 10, 4, 0, 0)),
                 ('end_date', None),
                 ('inout_cd', None),
                 ('location_cd', None),
                 ('location_path', None),
                 ('length_of_stay', None),
                 ('visit_blob', None),
                 ('update_date', datetime(2017, 1, 3, 0, 0)),
                 ('download_date', datetime(2017, 1, 3, 0, 0)),
                 ('import_date', datetime(2017, 1, 3, 0, 0)),
                 ('sourcesystem_cd', self._sourcesystem_cd),
                 ('upload_id', self._upload_id)]), as_dict(x))


if __name__ == '__main__':
    unittest.main()
