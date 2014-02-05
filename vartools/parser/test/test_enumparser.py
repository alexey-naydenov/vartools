"""Test enum parser on some examples."""

import os
from pprint import pprint

import vartools.parser.enumparser as vtep
import vartools.parser.utils as vtpu

#: Location of parser's test data.
_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def test_tracer_detector_log():
    """Check parser and dict functions on the sample file."""
    parser = vtep.EnumParser()
    code = open(os.path.join(_DATA_PATH, 'trace_codes.h')).read()
    enum_lists = vtpu.clean_enums(parser.parse(code))
    message_dict = vtpu.create_message_id_dict(enum_lists)
    assert message_dict[0].name == 'Error'
    assert message_dict[8].name == 'TaskId'
    type_dict = vtpu.create_type_id_dict(enum_lists)
    assert type_dict[32].name == 'TracerDetector'
    assert type_dict[33].name == 'ErrorEvents'
    assert type_dict[34].name == 'InfoEvents'
    assert type_dict[35].name == 'MessageEvents'
    assert type_dict[35].codes[0].name == 'Unspecified'
