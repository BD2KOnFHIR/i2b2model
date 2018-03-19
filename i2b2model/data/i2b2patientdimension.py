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
from datetime import datetime
from typing import Optional, Tuple, List

from dynprops import Local, Parent

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId
from i2b2model.sqlsupport.dbconnection import I2B2Tables


class VitalStatusCd:
    def __setattr__(self, key, value):
        if key not in ["birthcode", "deathcode"]:
            raise ValueError("New elements not allowed")
        super().__setattr__(key, value)

    class BirthDateCode:
        def __init__(self, code: str) -> None:
            self.code = code

    bd_unknown = BirthDateCode('L')
    bd_day = BirthDateCode('D')
    bd_month = BirthDateCode('B')
    bd_year = BirthDateCode('F')
    bd_hour = BirthDateCode('H')
    bd_minute = BirthDateCode('M')
    bd_second = BirthDateCode('C')

    class DeathDateCode:
        def __init__(self, code: str) -> None:
            self.code = code
    dd_living = DeathDateCode('N')
    dd_unknown = DeathDateCode('U')
    dd_deceased = DeathDateCode('Z')
    dd_day = DeathDateCode('Y')
    dd_month = DeathDateCode('M')
    dd_year = DeathDateCode('X')
    dd_hour = DeathDateCode('R')
    dd_minute = DeathDateCode('T')
    dd_second = DeathDateCode('S')

    def __init__(self, birth: BirthDateCode, death: DeathDateCode) -> None:
        self.birthcode = birth
        self.deathcode = death

    @property
    def code(self):
        return self.deathcode.code + self.birthcode.code

    def reify(self):
        return self.code

unknown_vital_status_cd = VitalStatusCd(VitalStatusCd.bd_unknown, VitalStatusCd.dd_unknown)

# TODO: should age be computed from birthdate / deathdate
# TODO: language code -- what do we do with this?

class PatientDimension(I2B2CoreWithUploadId):
    patient_num: Local[int]
    vital_status_cd: Local[Optional[VitalStatusCd]]
    birth_date: Local[Optional[datetime]]
    death_date: Local[Optional[datetime]]
    sex_cd: Local[Optional[str]]
    age_in_years_num: Local[Optional[int]]
    language_cd: Local[Optional[str]]
    race_cd: Local[Optional[str]]
    marital_status_cd: Local[Optional[str]]
    religion_cd: Local[Optional[str]]
    zip_cd: Local[Optional[str]]
    statecityzip_path: Local[Optional[str]]
    income_cd: Local[Optional[str]]
    patient_blob: Local[Optional[str]]
    _: Parent

    key_fields = ["patient_num"]

    def __init__(self, patient_num, vital_status_cd: Optional[VitalStatusCd]=unknown_vital_status_cd) -> None:
        self.patient_num = patient_num
        self.vital_status_cd = vital_status_cd

        super().__init__()

    @classmethod
    def delete_upload_id(cls, tables: I2B2Tables, upload_id: int) -> int:
        """
        Delete all patient_dimension records with the supplied upload_id
        :param tables: i2b2 sql connection
        :param upload_id: upload identifier to remove
        :return: number or records that were deleted
        """
        return cls._delete_upload_id(tables.crc_connection, tables.patient_dimension, upload_id)

    @classmethod
    def delete_sourcesystem_cd(cls, tables: I2B2Tables, sourcesystem_cd: str) -> int:
        """
        Delete all records with the supplied sourcesystem_cd
        :param tables: i2b2 sql connection
        :param sourcesystem_cd: sourcesystem_cd to remove
        :return: number or records that were deleted
        """
        return cls._delete_sourcesystem_cd(tables.crc_connection, tables.patient_dimension, sourcesystem_cd)

    @classmethod
    def add_or_update_records(cls, tables: I2B2Tables, records: List["PatientDimension"]) -> Tuple[int, int]:
        """
        Add or update the patient_dimension table as needed to reflect the contents of records
        :param tables: i2b2 sql connection
        :param records: records to apply
        :return: number of records added / modified
        """
        return cls._add_or_update_records(tables.crc_connection, tables.patient_dimension, records)
