from typing import Optional, List, Tuple

from dynprops import Local

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId
from i2b2model.sqlsupport.dbconnection import I2B2Tables


class EncounterIDEStatus:
    class EncounterIDEStatusCode:
        def __init__(self, code: str) -> None:
            self.code = code

        def reify(self):
            return self.code

    active = EncounterIDEStatusCode("A")
    inactive = EncounterIDEStatusCode("I")
    deleted = EncounterIDEStatusCode("D")
    merged = EncounterIDEStatusCode("M")


class EncounterMapping(I2B2CoreWithUploadId):
    encounter_ide: Local[str]
    encounter_ide_source: Local[str]
    project_id: Local[Optional[str]]
    encounter_num: Local[int]
    patient_ide: Local[str]
    patient_ide_source: Local[str]
    encounter_ide_status: Local[Optional[str]]

    key_fields = ["encounter_ide", "encounter_ide_source", "project_id", "patient_ide", "patient_ide_source"]

    def __init__(self,
                 encounter_ide: str,
                 encounter_ide_source: str,
                 project_id: str,
                 encounter_num: int,
                 patient_ide: str,
                 patient_ide_source: str,
                 encounter_ide_status: Optional[EncounterIDEStatus.EncounterIDEStatusCode]):
        self.encounter_ide = encounter_ide
        self.encounter_ide_source = encounter_ide_source
        self.project_id = project_id
        self.encounter_num = encounter_num
        self.patient_ide = patient_ide
        self.patient_ide_source = patient_ide_source
        self.encounter_ide_status = encounter_ide_status
        super().__init__()

    @classmethod
    def delete_upload_id(cls, tables: I2B2Tables, upload_id: int) -> int:
        """
        Delete all patient_dimension records with the supplied upload_id
        :param tables: i2b2 sql connection
        :param upload_id: upload identifier to remove
        :return: number or records that were deleted
        """
        return cls._delete_upload_id(tables.crc_connection, tables.encounter_mapping, upload_id)

    @classmethod
    def delete_sourcesystem_cd(cls, tables: I2B2Tables, sourcesystem_cd: str) -> int:
        """
        Delete all records with the supplied sourcesystem_cd
        :param tables: i2b2 sql connection
        :param sourcesystem_cd: sourcesystem_cd to remove
        :return: number or records that were deleted
        """
        return cls._delete_sourcesystem_cd(tables.crc_connection, tables.encounter_mapping, sourcesystem_cd)

    @classmethod
    def add_or_update_records(cls, tables: I2B2Tables, records: List["EncounterMapping"]) -> Tuple[int, int]:
        """
        Add or update the patient_dimension table as needed to reflect the contents of records
        :param tables: i2b2 sql connection
        :param records: records to apply
        :return: number of records added / modified
        """
        return cls._add_or_update_records(tables.crc_connection, tables.encounter_mapping, records)
