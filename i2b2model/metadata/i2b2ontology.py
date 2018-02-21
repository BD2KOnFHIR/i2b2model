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

from i2b2model.metadata.i2b2ontologyquery import Query
from i2b2model.metadata.i2b2ontologyvisualattributes import VisualAttributes
from i2b2model.shared.i2b2core import I2B2Core
from i2b2model.sqlsupport.dynobject import DynElements, DynObject, DynamicPropType


class OntologyEntry(I2B2Core):
    _t = DynElements(I2B2Core)
    ontology_name = "FHIR"

    def __init__(self,
                 c_full_name: str,
                 query: Query,
                 visualattributes: VisualAttributes = None,
                 c_basecode: Optional[str]=None,
                 update_date: Optional[DynamicPropType] = None,
                 download_date: Optional[DynamicPropType] = None,
                 sourcesystem_cd: Optional[DynamicPropType] = None,
                 import_date: Optional[DynamicPropType] = None):
        """
        Initialize an ontology entry.

        :param c_full_name: Full name of entry (e.g. '\\TEST\\class\\subclass\\...\\item\\')
        :param query: Dimension table query for item
        :param visualattributes: VisualAttributes for item
        :param c_basecode: "uri" for item
        :param update_date:
        :param download_date:
        :param sourcesystem_cd:
        :param import_date:
        """
        super().__init__(update_date, download_date, sourcesystem_cd, import_date)
        assert(c_full_name.endswith('\\'))
        self._c_fullname = c_full_name
        self._query = query
        self._visualattributes = visualattributes if visualattributes else VisualAttributes()
        self._c_basecode = c_basecode
        self._modifier_exclusion = False

    @DynObject.entry(_t)
    def c_hlevel(self) -> int:
        return self.c_fullname[:-1].count('\\') - 1

    @DynObject.entry(_t)
    def c_fullname(self) -> str:
        return self._c_fullname

    @DynObject.entry(_t)
    def c_name(self) -> str:
        return self.c_fullname[:-1].rsplit('\\', 1)[1]

    @DynObject.entry(_t)
    def c_synonym_cd(self) -> str:
        """ Two or more synonyms of each other will have the same c_basecode """
        return "N"

    @DynObject.entry(_t)
    def c_visualattributes(self) -> str:
        return str(self._visualattributes)

    @DynObject.entry(_t)
    def c_totalnum(self) -> Optional[int]:
        return None

    @DynObject.entry(_t)
    def c_basecode(self) -> Optional[str]:
        return self._c_basecode

    @DynObject.entry(_t)
    def c_metadataxml(self) -> Optional[str]:
        return None

    @DynObject.entry(_t)
    def c_facttablecolumn(self) -> str:
        return self._query.key

    @DynObject.entry(_t)
    def c_tablename(self) -> str:
        return self._query.table

    @DynObject.entry(_t)
    def c_columnname(self) -> str:
        return self._query.where_subj

    @DynObject.entry(_t)
    def c_columndatatype(self) -> str:
        return 'N' if self._query.numeric_key else 'T'

    @DynObject.entry(_t)
    def c_operator(self) -> str:
        return self._query.where_pred

    @DynObject.entry(_t)
    def c_dimcode(self) -> str:
        return self._query.where_obj

    @DynObject.entry(_t)
    def c_comment(self) -> Optional[str]:
        return None

    @DynObject.entry(_t)
    def c_tooltip(self) -> Optional[str]:
        return None

    @DynObject.entry(_t)
    def m_applied_path(self) -> str:
        return '@'

    DynObject._after_root(_t)

    @DynObject.entry(_t)
    def valuetype_cd(self) -> Optional[str]:
        return None

    @DynObject.entry(_t)
    def m_exclusion_cd(self) -> Optional[str]:
        return 'X' if self._modifier_exclusion else None

    @DynObject.entry(_t)
    def c_path(self) -> Optional[str]:
        # return self.basename[:-1].rsplit('\\', 1)[0]
        return None

    @DynObject.entry(_t)
    def c_symbol(self) -> Optional[str]:
        # return self.basename[:-1].rsplit('\\', 1)[1]
        return None

    def __lt__(self, other):
        return self.c_fullname + self.m_applied_path < other.c_fullname + self.m_applied_path

    def __eq__(self, other):
        return self.c_fullname + self.m_applied_path == other.c_fullname + self.m_applied_path
