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
from dynprops import DynProps, Local, Tuple, as_dict, List, Dict

from i2b2model.sqlsupport.i2b2tables import I2B2Tables


class Schemes(DynProps):
    c_key: Local[str]
    c_name: Local[str]
    c_description: Local[str]

    def __init__(self, key: str, name: str, description: str) -> None:
        self.c_key = key
        self.c_name = name
        self.c_description = description

    def _matches(self, d1: Dict[str, object], d2: Dict[str, object], ignore_keys: List[str]) -> bool:
        return all(d1[k] == d2[k] for k in d1.keys() if k not in ignore_keys)

    def exists(self, tables: I2B2Tables) -> bool:
        conn = tables.ont_connection
        table = tables.schemes
        return bool(list(conn.execute(table.select().where(table.c.c_key == self.c_key))))

    def del_record(self, tables: I2B2Tables) -> int:
        conn = tables.ont_connection
        table = tables.schemes
        return conn.execute(table.delete().where(table.c.c_key == self.c_key)).rowcount

    def add_or_update_record(self, tables: I2B2Tables) -> Tuple[int, int]:
        conn = tables.ont_connection
        table = tables.schemes
        numins, numupd = 0, 0
        rslt = list(conn.execute(table.select().where(table.c.c_key == self.c_key)))
        if rslt:
            for row in rslt:
                if not self._matches(row, as_dict(self), ['']):
                    conn.execute(table.update().where(table.c.c_key == self.c_key).values(as_dict(self)))
                    numupd = 1
        else:
            conn.execute(table.insert().values(as_dict(self)))
            numins = 1
        return numins, numupd
