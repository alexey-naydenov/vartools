"""VarTrace message parsing utilities."""

# pylint: disable=W0212

import struct
import logging

import vartools.common as vtc

_NAME_FORMAT_DICT = {'Int8': 'b', 'Uint8': 'B', 'Int16': 'h', 'Uint16': 'H',
                     'Int32': 'i', 'Uint32': 'I', 'Int64': 'q', 'Uint64': 'Q',
                     'Float': 'f', 'Double': 'd'}
_EVENT_TYPE_SUFFIX = 'Events'
_EVENT_TYPE_FORMAT = 'I'
_logger = logging.getLogger(__name__)


def _unpack_with(message, struct_object):
    """Unpack message data using unpacker object."""
    if not struct_object:
        return message
    if message.size < struct_object.size:
        _logger.error('Data size {0} is smaller then POD size {1}'.format(
            message.size, struct_object.size))
        return message
    if message.size % struct_object.size != 0:
        _logger.error('Data size {0} is not divisible by POD size {1}'.format(
            message.size, struct_object.size))
    if message.size == struct_object.size:
        value = struct_object.unpack(message.data)[0]
    else:
        value = [struct_object.unpack_from(message.data, offset)[0]
                 for offset in range(0, message.size, struct_object.size)]
    return message._replace(value=value)


def fill_pod_value(message, is_little=True):
    """Interpret data that corresponds to POD types.

    Fill value field of message based on data and type_id.

    :param message: message with empty value field.
    :type message: :class:`~vartools.tracereader.TraceMessage`
    :param bool is_little: encoding of data, little or big endian.
    """
    type_to_description = (vtc.TYPE_ID_FORMAT_DICT_LE if is_little
                           else vtc.TYPE_ID_FORMAT_DICT_BE)
    if message.type_id in type_to_description:
        struct_object = type_to_description[message.type_id]
        return _unpack_with(message, struct_object)
    else:
        return message


def fill_custom_value(message, type_id_dict):
    """Unpack value using struct object stored in type dictionary."""
    if message.type_id in type_id_dict:
        struct_object = type_id_dict[message.type_id].struct_object
        return _unpack_with(message, struct_object)
    return message


def get_value_description(message, type_id_dict):
    """Return value description or None.

    If message contains event codes and corresponding code was
    described then return this description.

    """
    if message.type_id in type_id_dict \
       and message.value in type_id_dict[message.type_id].codes:
        return type_id_dict[message.type_id].codes[message.value]
    return None


def data_to_text(data):
    """Convert binary data into textual representation."""
    byte_list = []
    for b in data:
        byte_list.append('{:02x}'.format(ord(b)))
    return ' '.join(byte_list)


def message_to_text(message, message_id_dict, type_id_dict):
    """Return message converted into a string."""
    message = fill_pod_value(message)
    message = fill_custom_value(message, type_id_dict)
    if message.message_id in message_id_dict:
        message_name = message_id_dict[message.message_id].name
    else:
        message_name = 'UknownMessage_{}'.format(message.message_id)
    if message.value is None:
        message_value = data_to_text(message.data)
    else:
        message_value = message.value
    value_desc = get_value_description(message, type_id_dict)
    if value_desc:
        message_value = value_desc.name
    return '{0:>10d} {1:20}{2}'.format(message.timestamp, message_name,
                                       message_value)


def collate_messages(message_iterable):
    """Collate messages by  """

def _data_to_value(message, type_ids, event_ids):
    # if type id is not among known types return
    if not message.type_id in type_ids:
        _logger.debug('Uknown type id: {}'.format(message.type_id))
        return data_to_text(message.data)
    # if type one of the standard types use struct to interpret
    type_name = type_ids[message.type_id].name
    if type_name in _NAME_FORMAT_DICT:
        value = struct.unpack(_DEFAULT_ENDIANESS + _NAME_FORMAT_DICT[type_name],
                              message.data)[0]
    # if type name follows event format read it as uint
    if type_name.endswith(_EVENT_TYPE_SUFFIX):
        value = struct.unpack(_DEFAULT_ENDIANESS + _EVENT_TYPE_FORMAT,
                              message.data)[0]
    # check if type is an event, convert to readable string then
    if message.type_id in type_ids \
            and type_ids[message.type_id].name.endswith(_EVENT_TYPE_SUFFIX):
        type_name = type_ids[message.type_id].name
        # replace event id with a string
        for event_list in event_ids:
            if type_name == event_list.name + _EVENT_TYPE_SUFFIX:
                if value in event_list.members:
                    value = event_list.members[value].name
                break
    return value

def message_to_dict(message, message_ids, type_ids, event_ids):
    result = {}
    result['timestamp'] = message.timestamp
    result['value'] = _data_to_value(message, type_ids, event_ids)
    result['message_id'] = message.message_id
    if message.message_id in message_ids:
        result['message'] = message_ids[message.message_id].name
    else: 
        result['message'] = message.message_id
    result['type_id'] = message.type_id
    if message.type_id in type_ids:
        result['type'] = type_ids[message.type_id].name
    else:
        result['type'] = message.type_id
    return result

def dict_to_clojure_map(dict_):
    terms = []
    for k, v in dict_.items():
        terms.append(':' + k)
        terms.append(str(v))
    return '{' + ' '.join(terms) + '}'

def message_to_clojure(message, message_ids, type_ids, event_ids):
    return dict_to_clojure_map(message_to_dict(
            message, message_ids, type_ids, event_ids))

if __name__ == '__main__':
    pass
