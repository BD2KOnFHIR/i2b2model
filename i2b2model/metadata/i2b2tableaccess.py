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
from typing import Optional

from dynprops import DynProps, Local

from i2b2model.metadata.i2b2ontologyquery import ConceptQuery, Query
from i2b2model.metadata.i2b2ontologyvisualattributes import VisualAttributes
from i2b2model.shared.tablenames import i2b2tablenames


class TableAccess(DynProps):
    c_table_cd: Local[str]
    c_table_name: Local[str] = i2b2tablenames.phys_name(i2b2tablenames.ontology_table)
    c_protected_access: Local[str] = "N"
    c_hlevel: Local[int]
    c_fullname: Local[str]
    c_name: Local[str]
    c_synonym_cd: Local[str] = "N"
    c_visualattributes: Local[str] = str(VisualAttributes("CA"))
    c_totalnum: Local[Optional[int]]
    c_basecode: Local[Optional[str]]
    c_metadataxml: Local[Optional[str]]
    c_facttablecolumn: Local[str] = lambda self: self._query.key
    c_dimtablename: Local[str] = lambda self: self._query.table
    c_columnname: Local[str] = lambda self: self._query.where_subj
    c_columndatatype: Local[str] = lambda self: 'N' if self._query.numeric_key else 'T'
    c_operator: Local[str] = lambda self: self._query.where_pred
    c_dimcode: Local[str] = lambda self: self._query.where_obj
    c_comment: Local[Optional[str]]
    c_tooltip: Local[Optional[str]] = lambda self: self.c_name
    c_entry_date: Local[Optional[str]]
    c_change_date: Local[Optional[str]]
    c_status_cd: Local[Optional[str]]
    valuetype_cd: Local[Optional[str]]

    def __init__(self, table_cd: str, fullname: Optional[str]=None, query: Optional[Query]=None,
                 hlevel: Optional[int]=None, name: Optional[str]=None) -> None:
        self.c_table_cd = table_cd
        self.c_fullname = fullname if fullname else f"\\{table_cd}\\"
        self._query = query if query else ConceptQuery(self._c_fullname)
        self.c_hlevel = hlevel if hlevel is not None else 1
        self.c_name = name if name else f"{self._c_table_cd} Resources"
