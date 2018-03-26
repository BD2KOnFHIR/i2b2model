from typing import Optional, Union

import datetime


class Query:
    """
    Representation of the query portion of an ontology table, including table, column, type, operator and code
    """
    def __init__(self,
                 table: str,
                 key: str,
                 numeric_key: bool,
                 where_subj: str,
                 where_pred: str,
                 where_obj: Optional[Union[int, str, datetime.datetime]]) -> None:
        assert where_pred != 'like' or not numeric_key, "'like' queries not allowed on numeric keys"
        if where_obj is not None:
            self.table = table
            self.key = key
            self.numeric_key = numeric_key
            self.where_subj = where_subj
            self.where_pred = where_pred
            self.where_obj = where_obj
        else:
            self.table = self.key = self.where_subj = self.where_pred = self.where_obj = ""
            self.numeric_key = False

    def __str__(self):
        where_text = "{where_obj}" if self.numeric_key else "'{where_obj}'"
        return ("SELECT {key}\nFROM {table}\n"
                "WHERE {where_subj} {where_pred} " + where_text).format(**self.__dict__)


class EmptyQuery(Query):
    """
    No query - default values for all the elements
    """
    def __init__(self) -> None:
        super().__init__("", "", False, "", "", "")

    def __str__(self):
        return "NO QUERY"


class ConceptQuery(Query):
    """
    A query for the concept dimension.   The only (typical) variable is the object of the WHERE clause.
    """
    def __init__(self, where_obj: str) -> None:
        """
        Concept dimension query.
        Usually: "SELECT concept_cd FROM concept_dimension WHERE concept_path LIKE {where_obj}
        In postgresql, 'LIKE' w/o percent signs is equivalent to '=' so '=' is never needed
        :param where_obj: path to match. If none, will be set to fullpath in ontology
        """
        super().__init__("concept_dimension",
                         "concept_cd",
                         False,
                         "concept_path",
                         "=",
                         where_obj)


class ModifierQuery(Query):
    """
    Modifier dimension query.  The only (typical) variable is the object of the WHERE clause.
    """
    def __init__(self, where_obj: str) -> None:
        """
        Modifier dimension query.
        Usually: "SELECT modifier_cd FROM modifier_dimension WHERE modifier_path LIKE {where_obj}"
        In postgresql, 'LIKE' w/o percent signs is equivalent to '=' so '=' is never needed
        :param where_obj: path to match. If none, will be set to fullpath in ontology
        """
        super().__init__("modifier_dimension",
                         "modifier_cd",
                         False,
                         "modifier_path",
                         "like",
                         where_obj)


class PatientQuery(Query):
    """ Patient Dimension Query """
    def __init__(self,
                 where_subj: str,
                 where_pred: str,
                 where_obj: Union[int, str, datetime.datetime],
                 numeric_obj: bool = True):
        """
        Patient dimension query.
        Usually: "SELECT patient_num FROM patient_dimension WHERE {where_subj} {where_pred} {where_obj}"
        :param where_subj: patient_dimenension column name
        :param where_pred: predicate (aka. operator)
        :param where_obj:  target
        :param numeric_obj: True means target is numeric (or datetime).  False means string w/ quotes.
        """
        super().__init__("patient_dimension",
                         "patient_num",
                         numeric_obj,
                         where_subj,
                         where_pred,
                         where_obj)


class VisitQuery(Query):
    def __init__(self,
                 where_subj: str,
                 where_pred: str,
                 where_obj: Union[int, str, datetime.datetime],
                 numeric_obj: bool = True):
        """
        Visit dimension query.
        Usually: "SELECT encounter_num FROM visit_dimension WHERE {where_subj} {where_pred} {where_obj}"
        :param where_subj: visit_dimension column name
        :param where_pred: predicate (aka. operator)
        :param where_obj:  target
        :param numeric_obj: True means target is numeric (or datetime).  False means string w/ quotes.
        """
        super().__init__("visit_dimension",
                         "encounter_num",
                         numeric_obj,
                         where_subj,
                         where_pred,
                         where_obj)


class ProviderQuery(Query):
    def __init__(self, where_obj) -> None:
        """
        Provider dimension query.
        Usually: "SELECT provider_id FROM provider_dimension WHERE provider_path LIKE {where_obj}"
        In postgresql, 'LIKE' w/o percent signs is equivalent to '=' so '=' is never needed
        :param where_obj: path to match
        """
        super().__init__("provider_dimension",
                         "provider_id",
                         False,
                         'provider_id',
                         'like',
                         where_obj)
