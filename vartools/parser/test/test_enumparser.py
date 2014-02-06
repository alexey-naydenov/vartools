"""Test enum parser on some examples."""

from __future__ import print_function
import os
import tables

import vartools.parser.enumparser as vtep
import vartools.parser.utils as vtpu
import vartools.tracereader as vttr
import vartools.messageutils as vtmu
import vartools.hdf5 as vthdf5

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


def test_tracer_detector_conversion():
    """Check conversion of tracer detector log."""
    test_print = print
    test_print = lambda x: x
    message_id_dict, type_id_dict = vtpu.parse_headers(
        [os.path.join(_DATA_PATH, 'trace_codes.h')], event_format='<i')
    #message_id_dict, type_id_dict = vtpu.parse_headers([])
    with open(os.path.join(_DATA_PATH, 'trace.bin'), 'rb') as trace_file:
        trace = vttr.TraceReader(trace_file)
        for message in trace:
            message = vtmu.fill_pod_value(message)
            message = vtmu.fill_custom_value(message, type_id_dict)
            if message.message_id in message_id_dict:
                message_name = message_id_dict[message.message_id].name
            else:
                message_name = 'UknownMessage_{}'.format(message.message_id)
            if message.value is None:
                message_value = vtmu.data_to_text(message.data)
            else:
                message_value = message.value
            value_desc = vtmu.get_value_description(message, type_id_dict)
            if value_desc:
                message_value = value_desc.name
            test_print(message_name)
            test_print(message_value)


def test_message_to_text():
    """Check conversion of tracer detector log to text."""
    test_print = print
    test_print = lambda x: x
    message_id_dict, type_id_dict = vtpu.parse_headers(
        [os.path.join(_DATA_PATH, 'trace_codes.h')], event_format='<i')
    #message_id_dict, type_id_dict = vtpu.parse_headers([])
    with open(os.path.join(_DATA_PATH, 'trace.bin'), 'rb') as trace_file:
        trace = vttr.TraceReader(trace_file)
        for message in trace:
            test_print(vtmu.message_to_text(message, message_id_dict,
                                            type_id_dict))


def test_collate_values():
    """Manually check collate values fucntions."""
    test_print = print
    test_print = lambda x: x
    _, type_id_dict = vtpu.parse_headers(
        [os.path.join(_DATA_PATH, 'trace_codes.h')], event_format='<i')
    #message_id_dict, type_id_dict = vtpu.parse_headers([])
    with open(os.path.join(_DATA_PATH, 'trace.bin'), 'rb') as trace_file:
        trace = vttr.TraceReader(trace_file)
        id_values_dict = vtmu.collate_values(
            (vtmu.fill_custom_value(vtmu.fill_pod_value(m), type_id_dict)
             for m in trace), lambda x: x*1e-9)
        test_print(id_values_dict)


def test_hdf5_export():
    """Create hdf5 file in tmp dir out of trace file."""
    message_desc_dict, type_desc_dict = vtpu.parse_headers(
        [os.path.join(_DATA_PATH, 'trace_codes.h')], event_format='<i')
    with open(os.path.join(_DATA_PATH, 'trace.bin'), 'rb') as trace_file:
        trace = vttr.TraceReader(trace_file)
        id_values_dict, message_type_dict = vtmu.collate_values(
            (vtmu.fill_custom_value(vtmu.fill_pod_value(m), type_desc_dict)
             for m in trace))
    h5file = tables.open_file('/tmp/vartools_test.h5', mode='w',
                              title='VarTools test file')
    trace_group = h5file.create_group('/', 'trace', 'Trace export test')
    vthdf5.export(h5file, trace_group, id_values_dict, message_type_dict,
                  message_desc_dict, type_desc_dict)
    h5file.close()
