"""Compare TraceReader output for samples with expected values."""

import os
import struct
import unittest as ut

import vartools.tracereader as vttr
import vartools.messageutils as vtmu
import vartools.common as vtc

#: Location of test data.
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def check_empty(trace):
    """Check that empty trace can be read without errors."""
    entries = [e for e in trace]
    assert(len(entries) == 0)


def check_integer_count(trace):
    """Check trace that contains int count from 0 to 999."""
    index = None
    for index, message in enumerate((vtmu.fill_pod_value(m) for m in trace)):
        assert message.value == index
    assert index == 999


def check_arrays(trace):
    """Check if integer arrays are correctly parsed."""
    for length in [10, 100, 1000]:
        array = vtmu.fill_pod_value(next(trace)).value
        assert array == list(range(length))


def check_int_sequence(trace):
    """Check if trace contains sequence of integers min, 0, 123, max."""
    message = vtmu.fill_pod_value(next(trace))
    assert message.type_id in vtc.TYPE_ID_FORMAT_DICT
    type_format = vtc.TYPE_ID_FORMAT_DICT[message.type_id]
    type_size = struct.calcsize(type_format)
    if type_format.islower():
        max_value = (1 << (type_size*8 - 1)) - 1
        min_value = -max_value - 1
    else:
        min_value = 0
        max_value = (1 << (type_size*8)) - 1
    assert message.value == min_value
    message = vtmu.fill_pod_value(next(trace))
    assert message.value == 0
    message = vtmu.fill_pod_value(next(trace))
    assert message.value == 123
    message = vtmu.fill_pod_value(next(trace))
    assert message.value == max_value


def check_float_sequence(trace):
    """Check if there are floats with min, 0, 123, max."""
    message = vtmu.fill_pod_value(next(trace))
    assert message.value > 0
    message = vtmu.fill_pod_value(next(trace))
    assert message.value == 0
    message = vtmu.fill_pod_value(next(trace))
    assert message.value == 123
    message = vtmu.fill_pod_value(next(trace))
    assert message.value > 0


def check_assorted_types(trace):
    """Check how different types are parsed.

    It is assumed that messages contain min, 0, 123, max values for
    each type.
    """
    for _ in range(8):
        check_int_sequence(trace)
    check_float_sequence(trace)
    check_float_sequence(trace)


#: Map test function to sample data file.
TEST_FUNCTION_FILE = [(check_empty, 'empty.bin'),
                      (check_integer_count, 'integer_count_1000.bin'),
                      (check_arrays, 'arrays_10_100_1000.bin'),
                      (check_assorted_types, 'assorted_types.bin')]


def test_samples():
    for function, filename in TEST_FUNCTION_FILE:
        with open(os.path.join(DATA_PATH, filename), 'rb') as sample:
            trace = vttr.TraceReader(sample)
            yield function, trace
