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
