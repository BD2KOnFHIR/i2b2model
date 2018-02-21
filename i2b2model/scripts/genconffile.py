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
from argparse import ArgumentParser
from typing import List

import os

import sys

conf_template = """-db postgresql+psycopg2://localhost:5432/i2b2
--user i2b2
--password demouser
"""


def generate_conf_file(argv: List[str]) -> bool:
    """
    Convert a set of FHIR resources into their corresponding i2b2 counterparts.

    :param argv: Command line arguments.  See: create_parser for details
    :return:
    """
    parser = ArgumentParser(description="Generate SQL db_conf file template")
    parser.add_argument("-f", "--configfile", help="File name to generate (Default: db_conf)", metavar="Config File",
                        default="db_conf")
    opts = parser.parse_args(argv)
    if os.path.exists(opts.configfile):
        print(f"{opts.configfile} already exists!")
        return False
    with open(opts.configfile, 'w') as f:
        f.write(conf_template)
    print(f"{opts.configfile} generated")
    return True


if __name__ == "__main__":
    if not generate_conf_file(sys.argv[1:]):
        sys.exit(1)
