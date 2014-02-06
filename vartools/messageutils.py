"""VarTrace message parsing utilities."""

# pylint: disable=W0212

from future.builtins import dict
import struct
import logging
from collections import defaultdict

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


def collate_values(messages, timestamp_to_time=None):
    """Collate messages values using message id.

    If value is None then it is skipped. Message ids are mapped to
    list of tuples of the form ``(timestamp, value)``.

    :param messages: an iterable that produce messages
    :type messages: :class:`~vartools.common.TraceMessage` list
    :return: two maps of message ids to lists of tuples and to type id
    :rtype: (dict, dict)

    """
    timestamp_to_time = timestamp_to_time if timestamp_to_time else lambda x: x
    collated_values = defaultdict(list)
    message_type_dict = dict()
    for message in messages:
        if message.value:
            collated_values[message.message_id].append(
                (timestamp_to_time(message.timestamp), message.value))
        if message.message_id in message_type_dict:
            if message.type_id != message_type_dict[message.message_id]:
                _logger.error(
                    'Different type ids correspond to the one message '
                    'id'.format(message.type_id,
                                message_type_dict[message.message_id]))
        else:
            message_type_dict[message.message_id] = message.type_id
    return collated_values, message_type_dict
