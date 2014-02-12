"""Conversion utilities."""

# pylint: disable=W0212

from datetime import datetime

import vartools.parser.utils as vtpu
import vartools.tracereader as vttr
import vartools.messageutils as vtmu
import vartools.hdf5 as vthdf5

_DEFAULT_EVENT_FORMAT = '<i'


def to_hdf5(h5file, group, trace_file, comment=None, headers=None,
            event_format=None):
    """Read trace file and store data into hdf5 format.

    :param group: list of strings with path to the trace group
    :param str comment: comment to the group
    :param list headers: paths to headers with trace description
    :param str event_format: valid ``struct`` format specifier
    """
    comment = comment if comment else ''
    headers = headers if headers else []
    event_format = event_format if event_format else _DEFAULT_EVENT_FORMAT
    message_desc_dict, type_desc_dict = vtpu.parse_headers(
        headers, event_format=event_format)
    trace = vttr.TraceReader(trace_file)
    id_values_dict, message_type_dict = vtmu.collate_values(
        (vtmu.fill_custom_value(vtmu.fill_pod_value(m), type_desc_dict)
         for m in trace))
    parent_group = '/' + '/'.join(group[:-1])
    trace_group = h5file.create_group(parent_group, group[-1], title=comment,
                                      createparents=True)
    trace_group._v_attrs.date = datetime.now().isoformat()
    vthdf5.export(h5file, trace_group, id_values_dict, message_type_dict,
                  message_desc_dict, type_desc_dict)
