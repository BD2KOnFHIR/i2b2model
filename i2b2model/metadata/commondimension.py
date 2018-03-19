# Copyright (c) 2018, Mayo Clinic
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
