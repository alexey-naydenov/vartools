import argparse
import logging

from vartools.parser.enumparser import EnumParser
from vartools.parser.utils import clean_enums, MESSAGE_CATEGORY_ID, \
    TYPE_CATEGORY_ID, EVENT_CATEGORY_ID
from vartools.tracereader import TraceReader
from vartools.messageutils import message_to_text, message_to_clojure


_logger = logging.getLogger(__name__)
_VERBOSITY_LOGLEVEL_DICT = {0: logging.ERROR, 1: logging.WARN,
                            2: logging.INFO, 3: logging.DEBUG}


def _create_argument_parser():
    argument_parser = argparse.ArgumentParser()
    # input and output parameters
    argument_parser.add_argument('-i', '--input', type=argparse.FileType('r'),
                                 default='-',
                                 help=('input file name, if not specified '
                                       'use stdin'))
    argument_parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                                 default='-',
                                 help=('output file name, if not specified '
                                       'use stdout'))
    argument_parser.add_argument('-c', '--cpp-header', nargs='+',
                                 help=('c++ header file names that describe '
                                       'trace ids'))
    argument_parser.add_argument('--clojure', action='count',
                                 help=('convert trace to clojure'))
    # verbosity level
    argument_parser.add_argument(
        "-v", "--verbosity", action="count", default=0,
        help="increase output verbosity")
    return argument_parser


def _parse_cpp_headers(headers):
    enum_parser = EnumParser()
    message_ids = {}
    type_ids = {}
    event_ids = []
    for header in headers:
        _logger.debug('Parsing cpp header: {}'.format(header))
        with open(header, 'r') as header_file:
            code = header_file.read()
            extracted_enums = clean_enums(enum_parser.parse(code))
            for enum in extracted_enums:
                if enum.category == MESSAGE_CATEGORY_ID:
                    message_ids.update(enum.members)
                if enum.category == TYPE_CATEGORY_ID:
                    type_ids.update(enum.members)
                if enum.category == EVENT_CATEGORY_ID:
                    event_ids.append(enum)
    return message_ids, type_ids, event_ids


def convert_vartrace():
    argument_parser = _create_argument_parser()
    arguments = argument_parser.parse_args()
    logging.basicConfig(
        level=_VERBOSITY_LOGLEVEL_DICT.get(arguments.verbosity, 3))
    if arguments.clojure:
        converter = message_to_clojure
    else:
        converter = message_to_text
    message_ids, type_ids, event_ids = _parse_cpp_headers(arguments.cpp_header)
    for m in TraceReader(arguments.input):
        arguments.output.write(converter(m, message_ids,
                                         type_ids, event_ids))
        arguments.output.write('\n')
