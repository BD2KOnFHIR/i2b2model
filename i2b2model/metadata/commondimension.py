from typing import List

from i2b2model.shared.i2b2core import I2B2CoreWithUploadId


class CommonDimension(I2B2CoreWithUploadId):
    """ Common base class of all dimensions """

    def __init__(self, name_prefix: str, subject: str, subject_name: str, subject_path: List[str],
                 base_path: str = '\\') -> None:
        """ Constructor

        :parem name_prefix: Namespace for concept code
        :param subject: subject concept code
        :param subject_name: subject name
        :param subject_path: path to subject - may or may not include subject as final element
        :param base_path: base path for all entries
        """
        super().__init__()
        assert(base_path.endswith('\\'))
        self._name_prefix = name_prefix
        self._subject = subject
        self._base_path = base_path
        self._subject_path = '\\'.join(subject_path if subject_path[-1] != subject else subject_path[:-1]) + '\\'
        self._name = subject_name

    def path(self) -> str:
        return self._base_path + self._subject_path + self._subject + '\\'

    def cd(self) -> str:
        return self._name_prefix + ':' + self._subject

    def name_char_(self) -> str:
        return self._name_prefix + ' ' + self._name

    @staticmethod
    def blob() -> str:
        return ''
