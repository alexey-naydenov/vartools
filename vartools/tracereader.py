import logging
import struct

from future.utils import implements_iterator

import vartools.common as vtc


@implements_iterator
class TraceReader:
    """Iterate over trace messages from given stream."""

    def __init__(self, stream, endianess=None):
        """Create object that spits out trace messages.

        :param io.RawIOBase stream: data source,
        :param str endianess: endianess string (see :mod:`struct`).
        """
        self._logger = logging.getLogger('TraceReader')
        self._stream = stream
        endianess = endianess if endianess else vtc.DEFAULT_ENDIANESS
        self._header_structure = [
            (name, endianess + field_format, struct.calcsize(field_format))
            for name, field_format in vtc.HEADER_STRUCTURE]
        self._subheader_structure = self._header_structure[1:]

    def __iter__(self):
        return self

    def _read_header(self):
        """Parse header and store in a dictionary.

        :return: dictionary with header fields.
        """
        log_entry = {}
        for field_name, field_format, field_size in self._header_structure:
            field_data = self._stream.read(field_size)
            if not field_data:
                if field_name != self._header_structure[0][0]:
                    self._logger.error(
                        'Reading stopped on field: {}'.format(field_name))
                raise StopIteration
            log_entry[field_name] = struct.unpack(field_format, field_data)[0]
        if log_entry['timestamp'] < 0:
            print('bad')
        return log_entry

    def _read_data(self, log_entry):
        """Read data from stream and add as a string to the dictionary.

        :param dict log_entry: dictionary with filled header fields.
        :return: dictionary with filled header, data and empty value fields.
        """
        log_entry['data'] = self._stream.read(log_entry['size'])
        if len(log_entry['data']) < log_entry['size']:
            self._logger.error('Data read failed: got {0} expected {1}'.format(
                len(log_entry['data']), log_entry['size']))
            raise StopIteration
        log_entry['value'] = None
        return log_entry

    def __next__(self):
        """Return next top level log entry.

        Iteration stops if no data can be read.
        """
        log_entry = self._read_header()
        log_entry = self._read_data(log_entry)
        if log_entry['size'] % vtc.ALIGNMENT_SIZE != 0:
            remainder = log_entry['size'] % vtc.ALIGNMENT_SIZE
            self._stream.read(vtc.ALIGNMENT_SIZE - remainder)
        return vtc.TraceMessage(**log_entry)
