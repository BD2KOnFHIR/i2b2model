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


class ObservationFactKey:
    def __init__(self, patient_num: int, encounter_num: int, provider_id: str,
                 start_date: Optional[datetime] = None) -> None:
        """
        A partial key to the observation fact table.  These three or four elements identify a collection of facts
        that can be added or replaced as a block

        :param patient_num: Patient number -- key to the patient_dimension table
        :param encounter_num: Encounter number -- key to the visit_dimension table
        :param provider_id: Provider identifier -- key to the provider_dimension table
        :param start_date: If provided, separates multiple entries w/ different dates of occurrence
        """
        self.patient_num = patient_num
        self.encounter_num = encounter_num
        self.provider_id = provider_id
        self.key_includes_start_date = start_date is not None
        self.start_date = start_date if start_date is not None else datetime.now()


class ValueTypeCd:
    def __init__(self, code: str) -> None:
        self.code = code

    def reify(self):
        return self.code


valuetype_text = ValueTypeCd('T')
valuetype_number = ValueTypeCd('N')
valuetype_blob = ValueTypeCd('B')
valuetype_nlp = ValueTypeCd('NLP')
valuetype_date = ValueTypeCd('D')
valuetype_novalue = ValueTypeCd('@')


class ObservationFact(I2B2CoreWithUploadId):
    encounter_num: Local[int]           # Link to encounter dimension - proxy for encounter id(e)
    patient_num: Local[int]             # Link to patient dimension - proxy for patient id(e)
    concept_cd: Local[str]              # Code for the observation of interest
    provider_id: Local[str]             # Practitioner or provider id
    start_date: Local[datetime]         # Starting date-time of observation (mm/dd/yy)
    modifier_cd: Local[str] = '@'       # Code for modifier of interest (e.g. Route, Dose)
    instance_num: Local[int] = 0        # Allows more than one modifier for each code
    valtype_cd: Local[Optional[str]] = '@'  # 'T' - text 'N' - number, 'B' blob, 'NLP' - NLP result, 'D - date
    tval_char: Local[Optional[str]]     # valtype_cd == 'T', text value, 'N', E, NE, L, LE, G, GE
    nval_num: Local[Optional[float]]    # Number when valtype_cd  == N
    valueflag_cd: Local[Optional[str]]  # 'X' - encrypted txt in blob column, 'H, 'L', 'A'
    quantity_num: Local[Optional[float]]    # Number of observations represented by this fact
    units_cd: Local[Optional[str]]
    end_date: Local[Optional[datetime]]     # Date that the observation ended - see addl' notes
    location_cd: Local[Optional[str]]       # Hospital associated with this visit
    observation_blob: Local[Optional[str]]  # XML data - partially or unstructeured data
    confidence_num: Local[Optional[float]]
    _: Parent

    key_fields = ["patient_num", "concept_cd", "modifier_cd", "start_date",
                  "encounter_num", "instance_num", "provider_id"]

    def __init__(self, fact_key: ObservationFactKey, concept_cd: str) -> None:
        super().__init__()
        self.patient_num = fact_key.patient_num
        self.encounter_num = fact_key.encounter_num
        self.provider_id = fact_key.provider_id
        self.concept_cd = concept_cd
        self.start_date = fact_key.start_date

    @property
    def pk(self) -> Tuple:
        return self.patient_num, self.encounter_num, self.instance_num,  self.concept_cd, self.modifier_cd

    def __lt__(self, other: "ObservationFact") -> bool:
        return self.pk < other.pk

    @classmethod
    def delete_upload_id(cls, tables: I2B2Tables, upload_id: int) -> int:
        """
        Delete all observation_fact records with the supplied upload_id
        :param tables: i2b2 sql connection
        :param upload_id: upload identifier to remove
        :return: number or records that were deleted
        """
        return cls._delete_upload_id(tables.crc_connection, tables.observation_fact, upload_id)

    @classmethod
    def delete_sourcesystem_cd(cls, tables: I2B2Tables, sourcesystem_cd: str) -> int:
        """
        Delete all records with the supplied sourcesystem_cd
        :param tables: i2b2 sql connection
        :param sourcesystem_cd: sourcesystem_cd to remove
        :return: number or records that were deleted
        """
        return cls._delete_sourcesystem_cd(tables.crc_connection, tables.observation_fact, sourcesystem_cd)

    @classmethod
    def add_or_update_records(cls, tables: I2B2Tables, records: List["ObservationFact"]) -> Tuple[int, int]:
        """
        Add or update the observation_fact table as needed to reflect the contents of records
        :param tables: i2b2 sql connection
        :param records: records to apply
        :return: number of records added / modified
        """
        return cls._add_or_update_records(tables.crc_connection, tables.observation_fact, records)

    def _date_val(self, dt: datetime) -> None:
        """
        Add a date value
        :param dt: datetime to add
        """
        self._tval_char = dt.strftime('%Y-%m-%d %H:%M')
        self._nval_num = (dt.year * 10000) + (dt.month * 100) + dt.day + \
                         (((dt.hour / 100.0) + (dt.minute / 10000.0)) if isinstance(dt, datetime) else 0)

    def summary(self) -> str:
        return f"({self.instance_num}, {self.concept_cd}, {self.modifier_cd}, {self.tval_char}, {self.nval_num})"
