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

from typing import List, Tuple, Optional

from dynprops import Local, Parent

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId
from i2b2model.sqlsupport.dbconnection import I2B2Tables


class PatientIDEStatus:
    class PatientIDEStatusCode:
        def __init__(self, code: str) -> None:
            self.code = code

        def reify(self):
            return self.code

    active = PatientIDEStatusCode("A")
    inactive = PatientIDEStatusCode("I")
    deleted = PatientIDEStatusCode("D")
    merged = PatientIDEStatusCode("M")



class PatientMapping(I2B2CoreWithUploadId):
    patient_ide: Local[str]
    patient_ide_source: Local[str]
    patient_num: Local[Optional[int]]
    patient_ide_status: Local[Optional[str]]
    project_id: Local[str]
    _: Parent

    key_fields = ["patient_ide", "patient_ide_source", "project_id"]

    def __init__(self, patient_num: int, patient_id: str, patient_ide_status: PatientIDEStatus.PatientIDEStatusCode,
                 patient_ide_source: str, project_id: str):
        """
        Construct a patient mapping entry
        :param patient_num: patient number
        :param patient_id: clear text patient identifier
        :param patient_ide_status: status code
        :param patient_ide_source: clear text patient identifier source
        :param project_id: project identifier

        The patient number is the key to the patient dimension file.  The patient_mapping file has, at a minimum,
        one entry
        """
        self.patient_num = patient_num
        self.patient_ide = patient_id
        self.patient_ide_status = patient_ide_status
        self.patient_ide_source = patient_ide_source
        self.project_id = project_id

        super().__init__()

    @classmethod
    def delete_upload_id(cls, tables: I2B2Tables, upload_id: int) -> int:
        """
        Delete all patient_mapping records with the supplied upload_id
        :param tables: i2b2 sql connection
        :param upload_id: upload identifier to remove
        :return: number or records that were deleted
        """
        return cls._delete_upload_id(tables.crc_connection, tables.patient_mapping, upload_id)

    @classmethod
    def delete_sourcesystem_cd(cls, tables: I2B2Tables, sourcesystem_cd: str) -> int:
        """
        Delete all records with the supplied sourcesystem_cd
        :param tables: i2b2 sql connection
        :param sourcesystem_cd: sourcesystem_cd to remove
        :return: number or records that were deleted
        """
        return cls._delete_sourcesystem_cd(tables.crc_connection, tables.patient_mapping, sourcesystem_cd)

    @classmethod
    def add_or_update_records(cls, tables: I2B2Tables, records: List["PatientMapping"]) -> Tuple[int, int]:
        """
        Add or update the patient_mapping table as needed to reflect the contents of records
        :param tables: i2b2 sql connection
        :param records: records to apply
        :return: number of records added / modified
        """
        return cls._add_or_update_records(tables.crc_connection, tables.patient_mapping, records)
