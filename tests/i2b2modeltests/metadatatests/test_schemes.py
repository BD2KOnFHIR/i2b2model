# Copyright (c) 2018, Mayo Clinic
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

from dynprops import as_dict, heading, row, OrderedDict

from i2b2model.metadata.i2b2schemes import Schemes
from tests.utils.connection_helper import connection_helper


class SchemesTestcase(unittest.TestCase):
    opts = connection_helper()
    rec = Schemes("TestCodeSystem", "A test coding system", "Used for unit tests - you should never see this")

    def setUp(self):
        self.rec.del_record(self.opts.tables)

    def tearDown(self):
        self.rec.del_record(self.opts.tables)

    def test_create(self):
        self.assertEqual("c_key\tc_name\tc_description", heading(self.rec))
        self.assertEqual('"TestCodeSystem"\t"A test coding system"\t"Used for unit tests - you should never see this"',
                         row(self.rec))
        self.assertEqual(OrderedDict([
             ('c_key', 'TestCodeSystem'),
             ('c_name', 'A test coding system'),
             ('c_description',
              'Used for unit tests - you should never see this')]), as_dict(self.rec))

        self.assertEqual((1, 0), self.rec.add_or_update_record(self.opts.tables))
        self.assertEqual((0, 0), self.rec.add_or_update_record(self.opts.tables))
        self.rec.c_description = "Used for tests"
        self.assertEqual((0, 1), self.rec.add_or_update_record(self.opts.tables))
        self.assertEqual(1, self.rec.del_record(self.opts.tables))
        self.assertEqual(0, self.rec.del_record(self.opts.tables))


if __name__ == '__main__':
    unittest.main()
