"""Constants and structures used in different modules."""

import struct

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
