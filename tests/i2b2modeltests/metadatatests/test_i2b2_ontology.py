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

import datetime
import unittest
from collections import OrderedDict


class OntologyTestCase(unittest.TestCase):
    def test_basics(self):
        from i2b2model.metadata.i2b2ontology import OntologyEntry
        from i2b2model.metadata.i2b2ontologyquery import ConceptQuery

        OntologyEntry.download_date = datetime.datetime(2017, 5, 25)
        OntologyEntry.sourcesystem_cd = "TEST"
        OntologyEntry.import_date = datetime.datetime(2017, 5, 25)
        OntologyEntry.update_date = datetime.datetime(2001, 12, 1)
        ontrec = OntologyEntry('\\X\\Y\\Z\\', ConceptQuery('\\X\\Y\\Z\\'), None, "17400008")
        self.assertEqual('c_hlevel\tc_fullname\tc_name\tc_synonym_cd\tc_visualattributes\t'
                         'c_totalnum\tc_basecode\tc_metadataxml\tc_facttablecolumn\tc_tablename\t'
                         'c_columnname\tc_columndatatype\tc_operator\tc_dimcode\tc_comment\t'
                         'c_tooltip\tm_applied_path\tupdate_date\tdownload_date\t'
                         'import_date\tsourcesystem_cd\tvaluetype_cd\tm_exclusion_cd\tc_path\tc_symbol',
                         ontrec._header())
        # Note that hierarchy level is zero based
        self.assertEqual(OrderedDict([
             ('c_hlevel', 2),
             ('c_fullname', '\\X\\Y\\Z\\'),
             ('c_name', 'Z'),
             ('c_synonym_cd', 'N'),
             ('c_visualattributes', 'FAE'),
             ('c_totalnum', None),
             ('c_basecode', '17400008'),
             ('c_metadataxml', None),
             ('c_facttablecolumn', 'concept_cd'),
             ('c_tablename', 'concept_dimension'),
             ('c_columnname', 'concept_path'),
             ('c_columndatatype', 'T'),
             ('c_operator', '='),
             ('c_dimcode', '\\X\\Y\\Z\\'),
             ('c_comment', None),
             ('c_tooltip', None),
             ('m_applied_path', '@'),
             ('update_date', datetime.datetime(2001, 12, 1, 0, 0)),
             ('download_date', datetime.datetime(2017, 5, 25, 0, 0)),
             ('import_date', datetime.datetime(2017, 5, 25, 0, 0)),
             ('sourcesystem_cd', 'TEST'),
             ('valuetype_cd', None),
             ('m_exclusion_cd', None),
             ('c_path', None),
             ('c_symbol', None)]), ontrec._freeze())


if __name__ == '__main__':
    unittest.main()
