
import unittest
from datetime import datetime, timedelta

from dynprops import as_dict, heading, clear

from i2b2model.data.i2b2patientdimension import VitalStatusCd
from i2b2model.shared.i2b2core import I2B2Core, I2B2CoreWithUploadId
from i2b2model.testingutils.base_test_case import BaseTestCase


class I2B2CoreTestCase(BaseTestCase):
    def setUp(self):
        clear(I2B2Core)
        clear(I2B2CoreWithUploadId)

    def tearDown(self):
        clear(I2B2Core)
        clear(I2B2CoreWithUploadId)

    def test_defaults(self):
        rtn = I2B2Core()
        rtnf = as_dict(rtn)
        self.assertAlmostNow(rtn.update_date)
        self.assertDatesAlmostEqual(rtn.update_date, str(rtnf['update_date']))
        self.assertAlmostNow(rtn.download_date)
        self.assertDatesAlmostEqual(rtn.download_date, str(rtnf['download_date']))
        self.assertAlmostNow(rtn.import_date)
        self.assertDatesAlmostEqual(rtn.import_date, str(rtnf['import_date']))
        self.assertEqual('Unspecified', rtn.sourcesystem_cd)
        self.assertEqual(rtn.sourcesystem_cd, rtnf['sourcesystem_cd'])
        self.assertEqual(['update_date', 'download_date', 'import_date', 'sourcesystem_cd'], list(rtnf.keys()))

        rtn = I2B2Core()
        I2B2Core.download_date = datetime(2009, 1, 1, 12, 0)
        I2B2Core.sourcesystem_cd = "MASTER"
        I2B2Core.import_date = datetime(2011, 1, 1, 12, 0)
        I2B2Core.update_date = datetime.now() + timedelta(hours=2)
        self.assertEqual('2009-01-01 12:00:00', str(rtn.download_date))
        self.assertEqual('2011-01-01 12:00:00', str(rtn.import_date))
        self.assertEqual('MASTER', rtn.sourcesystem_cd)
        self.assertDatesAlmostEqual(rtn.update_date, str(datetime.now() + timedelta(hours=2)))

        clear(I2B2Core)
        I2B2CoreWithUploadId.upload_id = 1777439
        rtn = I2B2CoreWithUploadId()
        if rtn.sourcesystem_cd != 'Unspecified':
            print("Caught it")
        self.assertEqual('Unspecified', rtn.sourcesystem_cd)
        self.assertEqual(1777439, rtn.upload_id)
        self.assertEqual('update_date\tdownload_date\timport_date\tsourcesystem_cd\tupload_id', heading(rtn))
        rtn = I2B2Core()
        with self.assertRaises(AttributeError):
            _ = rtn.upload_id

    def test_settings(self):
        clear(I2B2Core)
        I2B2Core.sourcesystem_cd = "abcd"
        I2B2Core.update_date = datetime(2014, 7, 31)
        I2B2Core.download_date = datetime.now
        rtn = I2B2Core()

        rtnf = as_dict(rtn)
        self.assertEqual(str(rtnf['update_date']), '2014-07-31 00:00:00')
        self.assertAlmostNow(rtn.download_date)
        self.assertEqual(rtn.update_date, rtn.import_date)
        self.assertEqual(rtnf['sourcesystem_cd'], 'abcd')
        self.assertEqual('update_date\tdownload_date\timport_date\tsourcesystem_cd', heading(rtn))

    def test_common_elements(self):
        """ Test the i2b2 core elements and demonstrate that they can't be overridden on an individual basis.

        These elements are:
            sourcesystem_cd = None
            update_date = None
            download_date = None
            import_date = None

        """
        from i2b2model.data.i2b2patientdimension import PatientDimension

        PatientDimension._clear()
        clear(I2B2CoreWithUploadId)
        pd = PatientDimension(111, VitalStatusCd('U', 'D'))

        I2B2Core.sourcesystem_cd = "abc"
        self.assertEqual("abc", pd.sourcesystem_cd)
        I2B2Core.update_date = datetime(2014, 7, 31)
        self.assertEqual(datetime(2014, 7, 31), pd.update_date)
        self.assertEqual(datetime(2014, 7, 31), pd.download_date)
        self.assertEqual(datetime(2014, 7, 31), pd.import_date)
        I2B2Core.download_date = datetime(2014, 7, 30)
        I2B2Core.import_date = datetime(2014, 7, 29)
        I2B2CoreWithUploadId.upload_id = 17

        self.assertEqual(datetime(2014, 7, 31), pd.update_date)
        self.assertEqual(datetime(2014, 7, 30), pd.download_date)
        self.assertEqual(datetime(2014, 7, 29), pd.import_date)

        self.assertEqual(17, pd.upload_id)

        PatientDimension._clear()
        self.assertEqual("abc", pd.sourcesystem_cd)
        clear(I2B2Core)
        self.assertEqual("Unspecified", pd.sourcesystem_cd)

    def test_common_setters(self):
        from i2b2model.shared.i2b2core import I2B2CoreWithUploadId
        from i2b2model.data.i2b2patientdimension import PatientDimension
        I2B2CoreWithUploadId.upload_id = 17
        with self.assertRaises(ValueError):
            PatientDimension.upload_id = 17


if __name__ == '__main__':
    unittest.main()
