"""Utilities for exporting into hdf5."""

import logging
import numpy as np
import tables

_logger = logging.getLogger(__name__)


def _get_hdf5_type(type_desc):
    """Try to figure out hdf5 type from type description.

    :param type_desc: type description
    :type type_desc: :class:`vartools.common.TypeDescription`
    :return: numpy type
    """
    return 'test'


def export(hdf5file, group, values, message_type_dict,
           message_desc_dict, type_desc_dict):
    """Export collated values into hdf5 file.

    :param hdf5file:
    :type hdf5file:
    :param group:
    :type group:
    :param values:
    :type values:
    :param message_type_dict:
    :type message_type_dict:
    :param message_desc_dict:
    :type message_desc_dict:
    :param type_desc_dict:
    :type type_desc_dict:
    """
    for message_id, values_list in values.items():
        type_desc = type_desc_dict[message_type_dict[message_id]]
        hdf5_type = _get_hdf5_type(type_desc)
        print(type_desc, hdf5_type)
