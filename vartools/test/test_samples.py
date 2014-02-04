"""Compare TraceReader output for samples with expected values."""

import os
import vartools.tracereader as vttr
import vartools.messageutils as vtmu

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


TEST_FUNCTION_FILE = [(check_empty, 'empty.bin'),
                      (check_integer_count, 'integer_count_1000.bin')]


def test_samples():
    for function, filename in TEST_FUNCTION_FILE:
        with open(os.path.join(DATA_PATH, filename), 'rb') as sample:
            trace = vttr.TraceReader(sample)
            yield function, trace
