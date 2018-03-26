from datetime import datetime
from typing import Optional, Tuple

from dynprops import DynProps, Local, as_dict

from i2b2model.metadata.i2b2ontologyquery import ConceptQuery, Query
from i2b2model.metadata.i2b2ontologyvisualattributes import VisualAttributes
from i2b2model.shared.tablenames import i2b2tablenames
from i2b2model.sqlsupport.i2b2tables import I2B2Tables


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
    c_entry_date: Local[Optional[str]] = datetime.now
    c_change_date: Local[Optional[str]]
    c_status_cd: Local[Optional[str]]
    valuetype_cd: Local[Optional[str]]

    def __init__(self, table_cd: str, fullname: Optional[str]=None, query: Optional[Query]=None,
                 hlevel: Optional[int]=None, name: Optional[str]=None) -> None:
        """ Create a table_access entry """
        self.c_table_cd = table_cd
        self.c_fullname = fullname if fullname else f"\\{table_cd}\\"
        self._query = query if query else ConceptQuery(self._c_fullname)
        self.c_hlevel = hlevel if hlevel is not None else 1
        self.c_name = name if name else f"{self._c_table_cd} Resources"

    @staticmethod
    def exists(c_table_cd: str, tables: I2B2Tables) -> int:
        """ Return the number of records that exist with the table code.
        - Ideally this should be zero or one, but the default table doesn't have a key

        :param c_table_cd: key to test
        :param tables:
        :return: number of records found
        """
        conn = tables.ont_connection
        table = tables.schemes
        return bool(list(conn.execute(table.select().where(table.c.c_table_cd == c_table_cd))))

    @staticmethod
    def del_records(c_table_cd: str, tables: I2B2Tables) -> int:
        """ Delete all records with c_table_code

        :param c_table_cd: key to delete
        :param tables:
        :return: number of records deleted
        """
        conn = tables.ont_connection
        table = tables.schemes
        return conn.execute(table.delete().where(table.c.c_table_cd == c_table_cd)).rowcount

    def add_or_update_record(self, tables: I2B2Tables) -> Tuple[int, int]:
        conn = tables.ont_connection
        table = tables.schemes
        numins, numupd = 0, 0
        rslt = list(conn.execute(table.select().where(table.c.c_table_cd == self.c_table_cd)))
        if rslt:
            for row in rslt:
                if row[1] != self.c_name or row[2] != self.c_description:
                    conn.execute(table.update().where(table.c.c_key == self.c_key).values(as_dict(self)))
                    numupd = 1
        else:
            conn.execute(table.insert().values(as_dict(self)))
            numins = 1
        return numins, numupd
