"""Constants and structures used in different modules."""

# pylint: disable=W0212

import struct
from collections import namedtuple

#: Map PODs onto struct module format character.
TYPE_ID_FORMAT_DICT = {1: 'b', 2: 'B', 3: 'h', 4: 'H',
                       5: 'i', 6: 'I', 7: 'q', 8: 'Q',
                       0xb: '?', 0xc: 'c', 0xf: 'f', 0xd: 'd'}

#: Map type id onto format descriptions (little endian serialization).
TYPE_ID_FORMAT_DICT_LE = {i: struct.Struct('<' + f)
                          for i, f in TYPE_ID_FORMAT_DICT.items()}

#: Map type id onto format descriptions (big endian serialization).
TYPE_ID_FORMAT_DICT_BE = {i: struct.Struct('>' + f)
                          for i, f in TYPE_ID_FORMAT_DICT.items()}


#: Enum members with description and values.
#: Fields: ``name`` - name of enum structure,
#: ``comment`` - last one line comment encountered
#: in the header file before enum definition,
#: ``members`` - map of enum values to enum member description,
#: ``category`` - one of possible enum categories:
#: :const:`UNKNOWN_CATEGORY_ID`, :const:`MESSAGE_CATEGORY_ID`,
#: :const:`TYPE_CATEGORY_ID`, :const:`EVENT_CATEGORY_ID`
EnumList = namedtuple('EnumList', 'name comment members category')

#: Named tuple to store name and comment together.
Description = namedtuple('Description', 'name comment')

#: Named tuple with type descriptions
TypeDescription = namedtuple('TypeDescription',
                             Description._fields + ('codes', 'struct_object'))

#: Set little endian as default.
DEFAULT_ENDIANESS = '<'
HEADER_STRUCTURE = [('timestamp', 'I'), ('size', 'H'),
                    ('message_id', 'B'), ('type_id', 'B')]
ALIGNMENT_SIZE = 4

#: Namedtuple to store header information, raw data and value
TraceMessage = namedtuple(
    'TraceMessage', ' '.join([n for n, f in HEADER_STRUCTURE]
                             + ['data', 'value']))
