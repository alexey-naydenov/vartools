"""VarTrace message parsing utilities."""

import struct
import logging


_DEFAULT_ENDIANESS = '<'

_NAME_FORMAT_DICT = {'Int8': 'b', 'Uint8': 'B', 'Int16': 'h', 'Uint16': 'H',
                     'Int32': 'i', 'Uint32': 'I', 'Int64': 'q', 'Uint64': 'Q',
                     'Float': 'f', 'Double': 'd'}
_EVENT_TYPE_SUFFIX = 'Events'
_EVENT_TYPE_FORMAT = 'I'
_logger = logging.getLogger(__name__)

def fill_value(message, type_ids):
    # if type id is not among known types return
    if not message.type_id in type_ids:
        _logger.debug('Uknown type id: {}'.format(message.type_id))
        return message
    # if type one of the standard types use struct to interpret
    type_name = type_ids[message.type_id].name
    if type_name in _NAME_FORMAT_DICT:
        value = struct.unpack(_DEFAULT_ENDIANESS + _NAME_FORMAT_DICT[type_name],
                              message.data)[0]
        message = message._replace(value=value)
    # if type name follows event format read it as uint
    if type_name.endswith(_EVENT_TYPE_SUFFIX):
        value = struct.unpack(_DEFAULT_ENDIANESS + _EVENT_TYPE_FORMAT,
                              message.data)[0]
        message = message._replace(value=value)
    return message

def data_to_text(data):
    byte_list = []
    for b in data:
        byte_list.append('0x{:02x}'.format(b))
    return ' '.join(byte_list)

def message_to_text(message, message_ids, type_ids, event_ids):
    # fill value field in message
    message = fill_value(message, type_ids)
    # convert timestamp
    timestamp = '{:10d}'.format(message.timestamp)
    # convert message name
    name = '{}:'
    if message.message_id in message_ids:
        name = name.format(message_ids[message.message_id].name)
    else:
        name = name.format('message_{}'.format(message.message_id))
    # convert value
    value = ''
    if message.value is None:
        value = data_to_text(message.data)
    else:
        value = '{}'.format(message.value)
        # check if type is an event
        if message.type_id in type_ids \
           and type_ids[message.type_id].name.endswith(_EVENT_TYPE_SUFFIX):
            type_name = type_ids[message.type_id].name
            # replace event id with a string
            for event_list in event_ids:
                if type_name == event_list.name + _EVENT_TYPE_SUFFIX:
                    if message.value in event_list.members:
                        value = event_list.members[message.value].name
                    break
    
    # join all parts together
    return ' '.join([timestamp, name, value])

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
