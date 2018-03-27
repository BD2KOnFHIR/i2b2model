
import unittest


class I2B2CodesTestCase(unittest.TestCase):

    def test_codes(self):
        from i2b2model.data.i2b2codes import I2B2DemographicsCodes
        self.assertEqual('DEM|AGE:-1', I2B2DemographicsCodes.age())
        self.assertEqual('DEM|AGE:17', I2B2DemographicsCodes.age(17))
        self.assertEqual('DEM|AGE:0', I2B2DemographicsCodes.age(0))
        self.assertEqual('DEM|DATE:birth', I2B2DemographicsCodes.birthdate)
        self.assertEqual('DEM|LANGUAGE:bulg', I2B2DemographicsCodes.language('bulg'))
        self.assertEqual('DEM|SEX:m', I2B2DemographicsCodes.sex_male)
        self.assertEqual('DEM|SEX:@', I2B2DemographicsCodes.sex_unknown)
        self.assertEqual('DEM|VITAL:y', I2B2DemographicsCodes.vital_dead)
        self.assertEqual('DEM|ZIP:55901', I2B2DemographicsCodes.zip(55901))

        self.assertEqual('DEM|SEX:m', I2B2DemographicsCodes().sex_male)


if __name__ == '__main__':
    unittest.main()
