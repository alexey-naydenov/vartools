#!/usr/bin/env python3

import sys
from contextlib import contextmanager

@contextmanager
def file_or_stdout(filename, *args, **kwargs):
    if filename:
        file_descriptor = open(filename, *args, **kwargs)
        try:
            yield file_descriptor
        finally:
            file_descriptor.close()
    else:
        yield sys.stdout

@contextmanager
def file_or_stdin(filename, *args, **kwargs):
    if filename:
        file_descriptor = open(filename, *args, **kwargs)
        try:
            yield file_descriptor
        finally:
            file_descriptor.close()
    else:
        yield sys.stdin
