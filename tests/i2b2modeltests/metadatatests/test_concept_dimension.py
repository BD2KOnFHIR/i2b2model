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

from dynprops import as_dict, heading

from i2b2model.shared.i2b2core import I2B2Core
from tests.utils.base_test_case import BaseTestCase


class ConceptDimensionTestCase(BaseTestCase):
    def setUp(self):
        I2B2Core._clear()

    def tearDown(self):
        I2B2Core._clear()

    def test_basics(self):
        from i2b2model.metadata.i2b2conceptdimension import ConceptDimension

        ConceptDimension._clear()
        I2B2Core.download_date = datetime(2017, 5, 25)
        I2B2Core.sourcesystem_cd = "TEST_SS"
        I2B2Core.import_date = datetime(2017, 5, 25)

        cd = ConceptDimension('TEST', 'root', 'Root test concept', ['L1', 'L2', 'root'], '\\TEST\\')
        self.assertAlmostNow(cd.update_date)
        I2B2Core.update_date = datetime(2001, 12, 1)
        expected = OrderedDict([('concept_path', '\\TEST\\L1\\L2\\root\\'),
                                ('concept_cd', 'TEST:root'),
                                ('name_char', 'TEST Root test concept'),
                                ('concept_blob', ''),
                                ('update_date', datetime(2001, 12, 1, 0, 0)),
                                ('download_date', datetime(2017, 5, 25, 0, 0)),
                                ('import_date', datetime(2017, 5, 25, 0, 0)),
                                ('sourcesystem_cd', 'TEST_SS'),
                                ('upload_id', None)])
        self.assertEqual(expected, as_dict(cd))

        # Note - balance is actually a modifier.  This is strictly an example
        cd = ConceptDimension('TEST', 'root', 'Root balance test concept', ['L1', 'L2', 'balance'], '\\TEST\\')
        expected = OrderedDict([('concept_path', '\\TEST\\L1\\L2\\balance\\root\\'),
                                ('concept_cd', 'TEST:root'),
                                ('name_char', 'TEST Root balance test concept'),
                                ('concept_blob', ''),
                                ('update_date', datetime(2001, 12, 1, 0, 0)),
                                ('download_date', datetime(2017, 5, 25, 0, 0)),
                                ('import_date', datetime(2017, 5, 25, 0, 0)),
                                ('sourcesystem_cd', 'TEST_SS'),
                                ('upload_id', None)])
        self.assertEqual(expected, as_dict(cd))

    def test_interactions(self):
        """
        ModifierDimension and ConceptDimension share a common root.  If the dynelements lists are not specific to the
        subclasses, we end up with one composite
        """
        from i2b2model.metadata.i2b2conceptdimension import ConceptDimension
        from i2b2model.metadata.i2b2modifierdimension import ModifierDimension

        self.assertEqual('modifier_path\tmodifier_cd\tname_char\tmodifier_blob\tupdate_date\t'
                         'download_date\timport_date\tsourcesystem_cd\tupload_id', heading(ModifierDimension))
        self.assertEqual('concept_path\tconcept_cd\tname_char\tconcept_blob\tupdate_date\t'
                         'download_date\timport_date\tsourcesystem_cd\tupload_id', heading(ConceptDimension))


if __name__ == '__main__':
    unittest.main()
