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
