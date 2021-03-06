import argparse
from argparse import Namespace
from typing import Callable, Optional

from .file_aware_parser import FileAwareParser
from i2b2model.shared.tablenames import i2b2tablenames, DEFAULT_ONTOLOGY_TABLE
from .i2b2tables import I2B2Tables


class ConfigFile(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs) -> None:
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser: FileAwareParser, namespace: Namespace, values, option_string=None):
        raise AttributeError("Must preprocess input arguments with decode_file_args function")


def add_connection_args(parser: FileAwareParser, strong_config_file: bool=True) -> FileAwareParser:
    """
    Add the database connection arguments to the supplied parser

    :param parser: parser to add arguments to
    :param strong_config_file: If True, force --conf to be processed.  This is strictly a test for programming errors,
      and has to be skipped due to removefacts function.
    :return: parser
    """
    # TODO: Decide what to do with this
    parser.add_file_argument("--conf", metavar="CONFIG FILE", help="Configuration file",
                             action=ConfigFile if strong_config_file else None)

    parser.add_argument("-db", "--dburl", help="Default database URL",
                        default=Default_DB_Connection)
    parser.add_argument("--user", help="Default user name",
                        default=Default_User)
    parser.add_argument("--password", help="Default password",
                        default=Default_Password)
    parser.add_argument("--crcdb", help="CRC database URL. (default: dburl)")
    parser.add_argument("--crcuser", help="User name for CRC database. (default: user)")
    parser.add_argument("--crcpassword", help="Password for CRC database. (default: password)")
    parser.add_argument("--ontodb", help="Ontology database URL.  (default: dburl)")
    parser.add_argument("--ontouser", help="User name for ontology database. (default: user)")
    parser.add_argument("--ontopassword", help="Password for ontology database. (default: password)")
    parser.add_argument("--onttable", metavar="ONTOLOGY TABLE NAME",
                        help="Ontology table name (default: {})".format(DEFAULT_ONTOLOGY_TABLE),
                        default=DEFAULT_ONTOLOGY_TABLE)
    return parser


def process_parsed_args(opts: Namespace, error_fun: Optional[Callable], connect: bool=True) -> Namespace:
    """
    Set the defaults for the crc and ontology schemas
    :param opts: parsed arguments
    :param error_fun: Function to call if error
    :param connect: actually connect. (For debugging)
    :return: namespace with additional elements added
    """
    def setdefault(vn: str, default: object) -> None:
        assert vn in opts, "Unknown option"
        if not getattr(opts, vn):
            setattr(opts, vn, default)

    if error_fun and \
            (getattr(opts, 'dburl') is None or getattr(opts, 'user') is None or getattr(opts, 'password') is None):
        error_fun("db url, user id and password must be supplied")
    setdefault('crcdb', opts.dburl)
    setdefault('crcuser', opts.user)
    setdefault('crcpassword', opts.password)
    setdefault('ontodb', opts.dburl)
    setdefault('ontouser', opts.user)
    setdefault('ontopassword', opts.password)
    if connect:
        opts.tables = I2B2Tables(opts)

    # TODO: This approach needs to be re-thought.  As i2b2tablenames is a singleton, any changes here
    # impact the entire testing harness
    if opts.onttable:
        i2b2tablenames.ontology_table = opts.onttable
    return opts


Default_DB_Connection = "postgresql+psycopg2://localhost:5432/i2b2"
Default_User = "postgres"
Default_Password = "postgres"
