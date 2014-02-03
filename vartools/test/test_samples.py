"""Compare TraceReader output for samples with expected values."""

import os
import vartools.tracereader as vttr

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def check_empty(trace):
    entries = [e for e in trace]
    assert(len(entries) == 0)


TEST_FUNCTION_FILE = [(check_empty, 'empty.bin')]


def test_samples():
    for function, filename in TEST_FUNCTION_FILE:
        with open(os.path.join(DATA_PATH, filename), 'rb') as sample:
            trace = vttr.TraceReader(sample)
            yield function, trace
