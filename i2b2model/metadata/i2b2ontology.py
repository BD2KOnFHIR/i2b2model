from typing import Optional

from dynprops import Local, Parent

from i2b2model.metadata.i2b2ontologyquery import Query, EmptyQuery
from i2b2model.metadata.i2b2ontologyvisualattributes import VisualAttributes
from i2b2model.shared.i2b2core import I2B2Core


class OntologyEntry(I2B2Core):
    c_hlevel: Local[int] = lambda self: self.c_fullname[:-1].count('\\') - 1 + self._hlevel_bias
    c_fullname: Local[str]
    c_name: Local[str] = lambda self: self.c_fullname[:-1].rsplit('\\', 1)[1]
    c_synonym_cd: Local[str] = "N"
    c_visualattributes: Local[str] = VisualAttributes()
    c_totalnum: Local[Optional[int]] = None
    c_basecode: Local[str]
    c_metadataxml: Local[Optional[str]] = None
    c_facttablecolumn: Local[str] = lambda self: self._query.key
    c_tablename: Local[str] = lambda self: self._query.table
    c_columnname: Local[str] = lambda self: self._query.where_subj
    c_columndatatype: Local[str] = lambda self: "N" if self._query.numeric_key else "T"
    c_operator: Local[str] = lambda self: self._query.where_pred
    c_dimcode: Local[str] = lambda self: self._query.where_obj
    c_comment: Local[Optional[str]] = None
    c_tooltip: Local[Optional[str]] = None
    m_applied_path: Local[str] = '@'
    _: Parent
    valuetype_cd: Local[Optional[str]] = None
    m_exclusion_cd: Local[Optional[str]] = lambda self: 'X' if self._modifier_exclusion else None
    c_path: Local[Optional[str]] = None
    c_symbol: Local[Optional[str]] = None

    base: str = "BASE"

    def __init__(self,
                 c_full_name: str,
                 query: Query,
                 visualattributes: VisualAttributes = None,
                 c_basecode: Optional[str]=None):
        """
        Initialize an ontology entry.

        :param c_full_name: Full name of entry (e.g. '\\TEST\\class\\subclass\\...\\item\\')
        :param query: Dimension table query for item
        :param visualattributes: VisualAttributes for item
        :param c_basecode: "uri" for item
        """
        super().__init__()
        assert(c_full_name.endswith('\\'))
        self.c_fullname = c_full_name
        self._query = query
        self._visualattributes = visualattributes if visualattributes else VisualAttributes()
        self.c_basecode = c_basecode
        self._modifier_exclusion = False
        self._hlevel_bias = 0

    def __lt__(self, other):
        return self.c_fullname + self.m_applied_path < other.c_fullname + self.m_applied_path

    def __eq__(self, other):
        return self.c_fullname + self.m_applied_path == other.c_fullname + self.m_applied_path
