
# TODO: The mapping portion of this function should be loaded from the i2b2 table mapping table
from typing import List

DEFAULT_ONTOLOGY_TABLE = "custom_meta"      # Default metadata ontology table


class _I2B2Tables:
    _funcs = {"phys_name", "all_tables"}

    def __init__(self) -> None:
        self.concept_dimension = None
        self.modifier_dimension = None
        self.table_access = None
        self.observation_fact = None
        self.ontology_table = DEFAULT_ONTOLOGY_TABLE
        self.patient_dimension = None
        self.patient_mapping = None
        self.visit_dimension = None
        self.provider_dimension = None
        self.encounter_mapping = None
        self.schemes = None

    def __getattribute__(self, item):
        """ Return the logical name of a table  """
        if item.startswith("_") or item not in self.__dict__:
            return super().__getattribute__(item)
        return self.__dict__[item] if item in _I2B2Tables._funcs else item

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def _clear(self):
        for k in self.all_tables():
            setattr(self, k, None if k != 'ontology_table' else DEFAULT_ONTOLOGY_TABLE)

    def phys_name(self, item: str) -> str:
        """Return the physical (mapped) name of item.

        :param item: logical table name
        :return: physical name of table
        """
        v = self.__dict__[item]
        return v if v is not None else item

    def all_tables(self) -> List[str]:
        """
        List of all known tables
        :return:
        """
        return sorted([k for k in self.__dict__.keys()
                       if k not in _I2B2Tables._funcs and not k.startswith("_")])


i2b2tablenames = _I2B2Tables()
