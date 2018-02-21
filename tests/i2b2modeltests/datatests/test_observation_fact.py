# Copyright (c) 2017, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
import unittest
from collections import OrderedDict
from datetime import datetime

from tests.utils.crc_testcase import CRCTestCase


class ObservationFactTestCase(CRCTestCase):

    def test_basics(self):
        from i2b2model.data.i2b2observationfact import ObservationFact, ObservationFactKey
        ObservationFact._clear()
        ObservationFact.update_date = datetime(2017, 2, 19, 12, 33)
        with self.sourcesystem_cd():
            ObservationFact.sourcesystem_cd = self._sourcesystem_cd
            ofk = ObservationFactKey(12345, 23456, 'provider', datetime(2017, 5, 23, 11, 17))
            x = ObservationFact(ofk, 'fhir:concept', sourcesystem_cd=self._sourcesystem_cd)
            self.assertEqual('encounter_num\tpatient_num\tconcept_cd\tprovider_id\tstart_date\tmodifier_cd\t'
                             'instance_num\tvaltype_cd\ttval_char\tnval_num\tvalueflag_cd\tquantity_num\tunits_cd\t'
                             'end_date\tlocation_cd\tobservation_blob\tconfidence_num\tupdate_date\tdownload_date\t'
                             'import_date\tsourcesystem_cd\tupload_id', x._header())
            self.assertEqual(OrderedDict([
                 ('encounter_num', 23456),
                 ('patient_num', 12345),
                 ('concept_cd', 'fhir:concept'),
                 ('provider_id', 'provider'),
                 ('start_date', datetime(2017, 5, 23, 11, 17)),
                 ('modifier_cd', '@'),
                 ('instance_num', 0),
                 ('valtype_cd', '@'),
                 ('tval_char', None),
                 ('nval_num', None),
                 ('valueflag_cd', None),
                 ('quantity_num', None),
                 ('units_cd', None),
                 ('end_date', None),
                 ('location_cd', None),
                 ('observation_blob', None),
                 ('confidence_num', None),
                 ('update_date', datetime(2017, 2, 19, 12, 33)),
                 ('download_date', datetime(2017, 2, 19, 12, 33)),
                 ('import_date', datetime(2017, 2, 19, 12, 33)),
                 ('sourcesystem_cd', self._sourcesystem_cd),
                 ('upload_id', None)]), x._freeze())


if __name__ == '__main__':
    unittest.main()
