
import unittest
from collections import OrderedDict
from datetime import datetime

from dynprops import heading, as_dict

from i2b2model.data.i2b2patientdimension import PatientDimension, VitalStatusCd
from i2b2model.shared.i2b2core import I2B2Core
from tests.utils.crc_testcase import CRCTestCase


class PatientDimensionTestCase(CRCTestCase):

    def test_basics(self):
        I2B2Core.update_date = datetime(2017, 1, 3)
        with self.sourcesystem_cd():
            I2B2Core.sourcesystem_cd = self._sourcesystem_cd
            x = PatientDimension(12345, VitalStatusCd(VitalStatusCd.bd_unknown, VitalStatusCd.dd_unknown))
            self.assertEqual('patient_num\tvital_status_cd\tbirth_date\tdeath_date\tsex_cd\tage_in_years_num\t'
                             'language_cd\trace_cd\tmarital_status_cd\treligion_cd\tzip_cd\tstatecityzip_path\t'
                             'income_cd\tpatient_blob\tupdate_date\tdownload_date\timport_date\t'
                             'sourcesystem_cd\tupload_id', heading(x))
            self.assertEqual(OrderedDict([
                 ('patient_num', 12345),
                 ('vital_status_cd', 'UL'),
                 ('birth_date', None),
                 ('death_date', None),
                 ('sex_cd', None),
                 ('age_in_years_num', None),
                 ('language_cd', None),
                 ('race_cd', None),
                 ('marital_status_cd', None),
                 ('religion_cd', None),
                 ('zip_cd', None),
                 ('statecityzip_path', None),
                 ('income_cd', None),
                 ('patient_blob', None),
                 ('update_date', datetime(2017, 1, 3, 0, 0)),
                 ('download_date', datetime(2017, 1, 3, 0, 0)),
                 ('import_date', datetime(2017, 1, 3, 0, 0)),
                 ('sourcesystem_cd', self._sourcesystem_cd),
                 ('upload_id', None)]), as_dict(x))
            x.birth_date = datetime(1955, 8, 10)
            x.death_date = datetime(2017, 9, 11)
            x.birth = VitalStatusCd.bd_day
            x.death = VitalStatusCd.dd_deceased
            x.sex_cd = "M"
            x.age_in_years = 62
            x.language_cd = 'english'
            x.race_cd = 'white'
            x.marital_status_cd = 'married'
            x.religion_cd = 'atheist'
            x.zip_cd = "55901-0138"
            x.statecityzip_path = 'Zip codes\\Minnesota\\Rochester\\55901\\'
            x.income_cd = "Medium"
            x.patient_blob = "<div>some text</div>"
            self.assertEqual(OrderedDict([
                 ('patient_num', 12345),
                 ('vital_status_cd', 'UL'),
                 ('birth_date', datetime(1955, 8, 10, 0, 0)),
                 ('death_date', datetime(2017, 9, 11, 0, 0)),
                 ('sex_cd', 'M'),
                 ('age_in_years_num', None),
                 ('language_cd', 'english'),
                 ('race_cd', 'white'),
                 ('marital_status_cd', 'married'),
                 ('religion_cd', 'atheist'),
                 ('zip_cd', '55901-0138'),
                 ('statecityzip_path', 'Zip codes\\Minnesota\\Rochester\\55901\\'),
                 ('income_cd', 'Medium'),
                 ('patient_blob', '<div>some text</div>'),
                 ('update_date', datetime(2017, 1, 3, 0, 0)),
                 ('download_date', datetime(2017, 1, 3, 0, 0)),
                 ('import_date', datetime(2017, 1, 3, 0, 0)),
                 ('sourcesystem_cd', self._sourcesystem_cd),
                 ('upload_id', None)]), as_dict(x))


if __name__ == '__main__':
    unittest.main()
