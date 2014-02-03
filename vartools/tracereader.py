import logging
import struct
from collections import namedtuple
from itertools import repeat
from operator import add

_DEFAULT_ENDIANESS = '<'
_SIZE_FIELD_NAME = 'size'
_HEADER_NAMES = ['timestamp', _SIZE_FIELD_NAME, 'message_id', 'type_id']
_HEADER_TYPES = ['I', 'H', 'B', 'B']
_DATA_FIELD_NAME = 'data'
_VALUE_FIELD_NAME = 'value'
_ALIGNMENT_SIZE = 4

TraceMessage = namedtuple('TraceMessage',
                          ' '.join(_HEADER_NAMES
                                   + [_DATA_FIELD_NAME, _VALUE_FIELD_NAME]))

class TraceReader:
    def __init__(self, stream):
        self._logger = logging.getLogger('TraceReader')
        self._stream = stream
        # prepend all struct types with endianess character
        self._header_types = list(map(add, repeat(_DEFAULT_ENDIANESS), 
                                      _HEADER_TYPES))
        self._header_names = _HEADER_NAMES

    def __iter__(self):
        return self

    def __next__(self):
        message = {}
        for field_name, field_type in zip(self._header_names,
                                          self._header_types):
            buffer = self._stream.read(struct.calcsize(field_type))
            if len(buffer) == 0:
                if field_name != self._header_names[0]:
                    self._logger.warn(
                        'Reading stopped on field: {}'.format(field_name))
                raise StopIteration
            message[field_name] = struct.unpack(field_type, buffer)[0]
        message[_DATA_FIELD_NAME] = self._stream.read(message[_SIZE_FIELD_NAME])
        # align next read
        if message[_SIZE_FIELD_NAME]%_ALIGNMENT_SIZE != 0:
            remainder = message[_SIZE_FIELD_NAME]%_ALIGNMENT_SIZE
            self._stream.read(_ALIGNMENT_SIZE - remainder)
        message[_VALUE_FIELD_NAME] = None
        return TraceMessage(**message)

if __name__ == '__main__':
    import sys
    # check if file name was given
    if len(sys.argv) != 2:
        print("Must provide filename")
        sys.exit()
    # set log level
    logging.basicConfig(level=logging.INFO)
    # open file
    with open(sys.argv[1], 'rb') as trace_file:
        for message in TraceReader(trace_file):
            if len(message) == 0:
                break
            print(message)
