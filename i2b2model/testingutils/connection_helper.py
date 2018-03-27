from argparse import Namespace

from i2b2model.sqlsupport.dbconnection import add_connection_args, process_parsed_args
from i2b2model.sqlsupport.file_aware_parser import FileAwareParser


def connection_helper(conf_file) -> Namespace:
    parser = FileAwareParser(description="Test connection")
    parser.add_argument("-l", "--load", help="Load i2b2 SQL tables", action="store_true")
    parser.add_argument("-u", "--uploadid", metavar="Upload identifier",
                        help="Upload identifer -- uniquely identifies this batch", type=int, required=True)
    opts = add_connection_args(parser)\
        .parse_args(parser.decode_file_args(['-u', '41712', '--conf', conf_file]))
    return process_parsed_args(opts, parser.error)
