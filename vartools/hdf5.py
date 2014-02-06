"""Utilities for exporting into hdf5."""

import logging
import functools
import tables

import vartools.common as vtc

_logger = logging.getLogger(__name__)

_FORMAT_COL_DICT = {'b': tables.Int8Col, 'B': tables.UInt8Col,
                    'h': tables.Int16Col, 'H': tables.UInt16Col,
                    'i': tables.Int32Col, 'I': tables.UInt32Col,
                    'q': tables.Int64Col, 'Q': tables.UInt64Col,
                    '?': tables.BoolCol, 'c': tables.StringCol,
                    'f': tables.Float32Col, 'd': tables.Float64Col}


def _get_col_type(type_id, type_desc_dict):
    """Try to figure out hdf5 type from type description.

    :param int type_id: trace type id
    :param type_desc_dict: map of type ids to type descriptions
    :type type_desc_dict: dict
    :return: tables.Col subclass
    """

    if type_id in vtc.TYPE_ID_FORMAT_DICT:
        return _FORMAT_COL_DICT[vtc.TYPE_ID_FORMAT_DICT[type_id]]
    if type_id not in type_desc_dict:
        _logger.error('No type description for type id {}'.format(type_id))
        return None
    if not type_desc_dict[type_id]:
        _logger.error('No format for type id {}'.format(type_id))
        return None
    if not type_desc_dict[type_id].codes:
        type_format = type_desc_dict[type_id].struct_object.format[1]
        return _FORMAT_COL_DICT[type_format]
    enum_dict = {v.name: k for k, v in type_desc_dict[type_id].codes.items()}
    enum_default = min(enum_dict, key=enum_dict.get)
    return functools.partial(tables.EnumCol, enum_dict, enum_default,
                             vtc.DEFAULT_ENUM_BASE)


def export(hdf5file, group, values, message_type_dict,
           message_desc_dict, type_desc_dict):
    """Export collated values into hdf5 file.

    :param hdf5file: hdf5 file object
    :param group: group in which trace tables will be created
    :type group: str or hdf5 group
    :param values: map of message types to list of (timestamp, value)
    :type values: dict
    :param message_type_dict:
    :type message_type_dict:
    :param message_desc_dict:
    :type message_desc_dict:
    :param type_desc_dict:
    :type type_desc_dict:
    """
    for message_id, values_list in values.items():
        if message_id not in message_desc_dict:
            _logger.error(
                'No description for message id {}'.format(message_id))
            continue
        type_id = message_type_dict[message_id]
        col_type = _get_col_type(type_id, type_desc_dict)
        if not col_type:
            continue
        table_format = {'time': tables.Time64Col(pos=0),
                        'value': col_type(pos=1)}
        data_table = hdf5file.create_table(
            group, message_desc_dict[message_id].name, table_format,
            message_desc_dict[message_id].comment)
        data_table.append(values_list)
