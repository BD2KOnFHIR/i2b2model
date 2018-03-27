

import unittest
from datetime import datetime

from i2b2model.data.i2b2encountermapping import EncounterMapping
from i2b2model.shared.i2b2core import I2B2Core, I2B2CoreWithUploadId
from i2b2model.testingutils.connection_helper import connection_helper
from tests.utils.crc_testcase import CRCTestCase


class EncounterMappingSQLTest(CRCTestCase):
    opts = connection_helper(CRCTestCase.test_conf_file)

    def test_insert(self):
        from i2b2model.data.i2b2encountermapping import EncounterIDEStatus

        I2B2Core.update_date = datetime(2017, 5, 25)

        with self.sourcesystem_cd():
            I2B2Core.sourcesystem_cd = self._sourcesystem_cd
            I2B2CoreWithUploadId.upload_id = self._upload_id

            # Add a brand new encounter mapping entry
            EncounterMapping.delete_sourcesystem_cd(self.opts.tables, self._sourcesystem_cd)
            em = EncounterMapping("f001x", "http://hl7.org/fhir", "FHIR", 1005000017, "patient01x",
                                  "http://hl7.org/fhir", EncounterIDEStatus.active)

            n_ins, n_upd = EncounterMapping.add_or_update_records(self.opts.tables, [em])
            self.assertEqual((0, 1), (n_upd, n_ins))
            n_ins, n_upd = EncounterMapping.add_or_update_records(self.opts.tables, [em])
            self.assertEqual((0, 0), (n_upd, n_ins))

            # Modify one entry and add a second
            em.encounter_ide_status = EncounterIDEStatus.inactive
            em2 = EncounterMapping("f002x", "http://hl7.org/fhir", "FHIR", 1005000018, "patient01x",
                                   "http://hl7.org/fhir", EncounterIDEStatus.active)
            n_ins, n_upd = EncounterMapping.add_or_update_records(self.opts.tables, [em, em2])
            self.assertEqual((1, 1), (n_upd, n_ins))
            self.assertEqual(2, EncounterMapping.delete_upload_id(self.opts.tables, self._upload_id))


if __name__ == '__main__':
    unittest.main()
