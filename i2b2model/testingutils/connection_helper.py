from argparse import Namespace
from typing import List

from i2b2model.sqlsupport.dbconnection import add_connection_args, process_parsed_args
from i2b2model.sqlsupport.file_aware_parser import FileAwareParser


def create_parser() -> FileAwareParser:
    """ Create a parser for unit testing """
    parser = FileAwareParser(description="Test connection")
    parser.add_argument("-l", "--load", help="Load i2b2 SQL tables", action="store_true")
    parser.add_argument("-u", "--uploadid", metavar="Upload identifier",
                        help="Upload identifer -- uniquely identifies this batch", type=int, required=True)
    return add_connection_args(parser)


def parse_args(parser: FileAwareParser, upload_id: int, conf_file: str, addl_args: List[str]) -> Namespace:
    """ Add the basic unit test arguments

    :param parser: parser to add args to
    :param upload_id: Upload id to use in config
    :param conf_file: location of configuration file
    :param addl_args: additional arguments to add to parser
    :return: Parsed arguments
    """
    return parser.parse_args(parser.decode_file_args(['-u', str(upload_id), '--conf', conf_file] + addl_args))


def connection_helper(conf_file: str) -> Namespace:
    return process_parsed_args(parse_args(create_parser(), 41712, conf_file, []), FileAwareParser.error)
