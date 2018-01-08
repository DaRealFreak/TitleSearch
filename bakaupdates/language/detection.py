#!/usr/local/bin/python
# coding: utf-8
import binascii
import re

import numpy as np

from bakaupdates.language import LanguageTemplate


def extract_unicode_characters(string):
    """Escape all unicode characters and return a generator for the int values of the unicode characters

    :param string:
    :return:
    """
    unicode_characters = re.findall(b'\\\\u([a-f0-9]{4})', string.encode('unicode_escape'))
    for x in unicode_characters:
        s = binascii.unhexlify(x)
        yield int.from_bytes(s, byteorder='big')


def matches_language(title, language):
    """Determine based on unicode elements, if the title matches the language pattern.

    :param title:
    :param language:
    :return:
    """
    if not issubclass(language, LanguageTemplate):
        raise EnvironmentError("{0:s} is not a subclass of the language template".format(language.__name__))

    unicode_characters = list(extract_unicode_characters(title))
    if language.requires_unicode_characters and not unicode_characters:
        return False

    if language.forbids_unicode_characters and unicode_characters:
        return False

    # not sure but all titles I found so far have a clear character set, not shared
    # noinspection PyTypeChecker
    return all([np.any((language.unicode_character_lowers <= int(unichar)) &
                       (int(unichar) <= language.unicode_character_uppers)) for unichar in unicode_characters])
