#!/usr/local/bin/python
# coding: utf-8

import binascii
import re
from typing import Generator, Type

import numpy as np

from titlesearch.language import LanguageTemplate


def extract_unicode_characters(string: str) -> Generator:
    """Escape all unicode characters and return a generator for the int values of the unicode characters

    :type string: str
    :return:
    """
    unicode_characters = re.findall(b'\\\\u([a-f0-9]{4})', string.encode('unicode_escape'))
    for x in unicode_characters:
        s = binascii.unhexlify(x)
        yield int.from_bytes(s, byteorder='big')


def matches_language(title: str, language: Type[LanguageTemplate]) -> bool:
    """Determine based on unicode elements, if the title matches the language pattern.

    :type title: str
    :type language: LanguageTemplate
    :return:
    """
    unicode_characters = list(extract_unicode_characters(title))
    if language.requires_unicode_characters and not unicode_characters:
        return False

    if language.forbids_unicode_characters and unicode_characters:
        return False

    # not sure but all titles I found so far have a clear character set, not shared
    # noinspection PyTypeChecker
    return all([np.any((language.unicode_character_lowers <= int(unichar)) &
                       (int(unichar) <= language.unicode_character_uppers)) for unichar in unicode_characters])
