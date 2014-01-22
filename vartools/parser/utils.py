#!/usr/bin/env python3

from collections import namedtuple


UNKNOWN_CATEGORY_ID = 0
MESSAGE_CATEGORY_ID = 1
TYPE_CATEGORY_ID = 2
EVENT_CATEGORY_ID = 3

CATEGORY_SUFFIX_DICT = {MESSAGE_CATEGORY_ID: 'MessageIds',
                        TYPE_CATEGORY_ID: 'TypeIds',
                        EVENT_CATEGORY_ID: 'Events'}

CATEGORY_MEMBER_PREFIX_DICT = {UNKNOWN_CATEGORY_ID: '',
                               MESSAGE_CATEGORY_ID: 'kMessageId',
                               TYPE_CATEGORY_ID: 'kTypeId',
                               EVENT_CATEGORY_ID: 'k{}Event'}

Description = namedtuple('Description', 'name comment')
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
    cleaned_enums = []
    for e in enums:
        cleaned_enums.append(clean_member_names(fill_category(e)))

    return cleaned_enums
