import logging
import struct
from collections import namedtuple

from future.utils import implements_iterator

_DEFAULT_ENDIANESS = '<'
_HEADER_STRUCTURE = [('timestamp', 'I'), ('size', 'H'),
                     ('message_id', 'B'), ('type_id', 'B')]
_ALIGNMENT_SIZE = 4

TraceMessage = namedtuple(
    'TraceMessage', ' '.join([n for n, f in _HEADER_STRUCTURE]
                             + ['data', 'value']))


@implements_iterator
class TraceReader:
    def __init__(self, stream, endianess=None):
        self._logger = logging.getLogger('TraceReader')
        self._stream = stream
        endianess = endianess if endianess else _DEFAULT_ENDIANESS
        self._header_structure = [
            (name, endianess + field_format, struct.calcsize(field_format))
            for name, field_format in _HEADER_STRUCTURE]
        self._subheader_structure = self._header_structure[1:]

    def __iter__(self):
        return self

    def _read_header(self):
        log_entry = {}
        for field_name, field_format, field_size in self._header_structure:
            field_data = self._stream.read(field_size)
            if not field_data:
                if field_name != self._header_structure[0][0]:
                    self._logger.error(
                        'Reading stopped on field: {}'.format(field_name))
                raise StopIteration
            log_entry[field_name] = struct.unpack(field_format, field_data)[0]
        return log_entry

    def _read_data(self, log_entry):
        log_entry['data'] = self._stream.read(log_entry['size'])
        if len(log_entry['data']) < log_entry['size']:
            self._logger.error('Data read failed: got {0} expected {1}'.format(
                len(log_entry['data']), log_entry['size']))
            raise StopIteration
        return log_entry

    def __next__(self):
        log_entry = self._read_header()
        log_entry = self._read_data(log_entry)
        if log_entry['size'] % _ALIGNMENT_SIZE != 0:
            remainder = log_entry['size'] % _ALIGNMENT_SIZE
            self._stream.read(_ALIGNMENT_SIZE - remainder)
        log_entry['value'] = None
        return TraceMessage(**log_entry)
