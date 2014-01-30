# pylint: disable=W0212

from collections import namedtuple

#: Enum that does not belong to any category.
UNKNOWN_CATEGORY_ID = 0
#: Enum with message ids.
MESSAGE_CATEGORY_ID = 1
#: Enum list with type ids.
TYPE_CATEGORY_ID = 2
#: Enum list with event ids.
EVENT_CATEGORY_ID = 3

CATEGORY_SUFFIX_DICT = {MESSAGE_CATEGORY_ID: 'MessageIds',
                        TYPE_CATEGORY_ID: 'TypeIds',
                        EVENT_CATEGORY_ID: 'Events'}

CATEGORY_MEMBER_PREFIX_DICT = {UNKNOWN_CATEGORY_ID: '',
                               MESSAGE_CATEGORY_ID: 'kMessageId',
                               TYPE_CATEGORY_ID: 'kTypeId',
                               EVENT_CATEGORY_ID: 'k{}Event'}

#: Named tuple to store name and comment together.
Description = namedtuple('Description', 'name comment')

#: Enum members with description and values.
#: Fields: ``name`` - name of enum structure,
#: ``comment`` - last one line comment encountered
#: in the header file before enum definition,
#: ``members`` - map of enum values to enum member description,
#: ``category`` - one of possible enum categories:
#: :const:`UNKNOWN_CATEGORY_ID`, :const:`MESSAGE_CATEGORY_ID`,
#: :const:`TYPE_CATEGORY_ID`, :const:`EVENT_CATEGORY_ID`
EnumList = namedtuple('EnumList', 'name comment members category')


def fill_category(enum_list):
    result_enum = enum_list._replace(category=UNKNOWN_CATEGORY_ID)
    for category, suffix in CATEGORY_SUFFIX_DICT.items():
        if enum_list.name.endswith(suffix):
            new_name = enum_list.name[:-len(suffix)]
            result_enum = enum_list._replace(
                category=category)._replace(name=new_name)
            break
    return result_enum


def clean_member_names(enum_list):
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
