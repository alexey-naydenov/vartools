# pylint: disable=W0212

import logging
import struct
from future.builtins import dict

import vartools.common as vtc
import vartools.parser.enumparser as vtep

#: Enum that does not belong to any category.
UNKNOWN_CATEGORY_ID = 0
#: Enum with message ids.
MESSAGE_CATEGORY_ID = 1
#: Enum list with type ids.
TYPE_CATEGORY_ID = 2
#: Enum list with event ids.
EVENT_CATEGORY_ID = 3

#: Map of enum categories to enum name endings.
CATEGORY_SUFFIX_DICT = {MESSAGE_CATEGORY_ID: 'MessageIds',
                        TYPE_CATEGORY_ID: 'TypeIds',
                        EVENT_CATEGORY_ID: 'Events'}

#: Enum members prefix templates.
CATEGORY_MEMBER_PREFIX_DICT = {UNKNOWN_CATEGORY_ID: '',
                               MESSAGE_CATEGORY_ID: 'kMessageId',
                               TYPE_CATEGORY_ID: 'kTypeId',
                               EVENT_CATEGORY_ID: 'k{}Event'}

_logger = logging.getLogger(__name__)


def fill_category(enum_list):
    """Try to figure out enum category from name.

    Using :const:`CATEGORY_SUFFIX_DICT` and enum name ending
    fill ``category`` field of :class:`EnumList`. The ending is
    chopped off if category is identified.

    :param enum_list: enum description
    :type enum_list: :class:`EnumList`

    """

    result_enum = enum_list._replace(category=UNKNOWN_CATEGORY_ID)
    for category, suffix in CATEGORY_SUFFIX_DICT.items():
        if enum_list.name.endswith(suffix):
            new_name = enum_list.name[:-len(suffix)]
            result_enum = enum_list._replace(
                category=category)._replace(name=new_name)
            break
    return result_enum


def clean_member_names(enum_list):
    """Remove repeating prefixes from enum members.

    If entries of an categorized enum start with the category
    specific suffix then remove it.

    :param enum_list: enum description
    :type enum_list: :class:`EnumList`

    """

    prefix = CATEGORY_MEMBER_PREFIX_DICT[enum_list.category].format(
        enum_list.name)
    cleaned_members = {}
    for member_id, member_description in enum_list.members.items():
        if member_description.name.startswith(prefix):
            cleaned_name = member_description.name[len(prefix):]
            member_description = member_description._replace(name=cleaned_name)
        cleaned_members[member_id] = member_description
    return enum_list._replace(members=cleaned_members)


def clean_enums(enums):
    """Apply :func:`clean_member_names` and :func:`fill_category` to enums.

    :param enums: list of enums to clean.
    :type enums: list of :class:`EnumList`

    """

    return [clean_member_names(fill_category(e)) for e in enums]


def create_message_id_dict(enums):
    """Extract message ids from enums and store in a dictionary.

    :param enums: list of enums processed by :func:`clean_enums`
    :type enums: list of :class:`EnumList`
    """

    id_dict = dict()
    for enum in enums:
        if enum.category != MESSAGE_CATEGORY_ID:
            continue
        overlapping_keys = enum.members.keys() & id_dict.keys()
        if overlapping_keys:
            _logger.error('Overlapping keys: {0}'.format(
                ', '.join(overlapping_keys)))
        id_dict.update(enum.members)
    return id_dict


def create_type_id_dict(enums, event_format=None):
    """Create dictionary with type id descriptions.

    It is assumed that some types contain event codes. This function
    looks for enums that correspond to event codes and create
    dictionary that maps ``type_id`` to these event codes. It assumes
    that if there is a type with the name ``SomethingEvents`` then
    enum with name ``Something`` contains event codes.

    :param enums: list of enums processed by :func:`clean_enums`
    :type enums: list of :class:`EnumList`
    :param str event_format: ``struct`` format string to parse event codes

    """
    # construct type dict
    type_dict = dict()
    for e in enums:
        if e.category != TYPE_CATEGORY_ID:
            continue
        overlapping_keys = e.members.keys() & type_dict.keys()
        if overlapping_keys:
            _logger.error('Overlapping keys: {0}'.format(
                ', '.join(overlapping_keys)))
        for type_id, desc in e.members.items():
            struct_object = None
            if event_format and desc.name.endswith(
                    CATEGORY_SUFFIX_DICT[EVENT_CATEGORY_ID]):
                struct_object = struct.Struct(event_format)
            type_desc = vtc.TypeDescription(
                name=desc.name, comment=desc.comment,
                codes=dict(), struct_object=struct_object)
            type_dict[type_id] = type_desc
    # fill codes
    for e in enums:
        if e.category != EVENT_CATEGORY_ID:
            continue
        type_name = e.name + CATEGORY_SUFFIX_DICT[EVENT_CATEGORY_ID]
        for type_id, type_desc in type_dict.items():
            if type_name != type_desc.name:
                continue
            type_desc.codes.update(e.members)
    return type_dict


def parse_headers(headers, **kwargs):
    """Parse headers and return message_id and type_id dictionaries.

    :param headers: list of paths to headers
    :type headers: str list
    :return: message_id and type_id dictionaries
    :rtype: (dict, dict)
    """
    parser = vtep.EnumParser()
    enum_lists = []
    for header in headers:
        header_code = open(header).read()
        enum_lists.extend(clean_enums(parser.parse(header_code)))
    message_dict = create_message_id_dict(enum_lists)
    type_dict = create_type_id_dict(enum_lists, **kwargs)
    return message_dict, type_dict
