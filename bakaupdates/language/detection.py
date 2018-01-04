#!/usr/local/bin/python
# coding: utf-8
import binascii
import re

import numpy as np


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
    unicode_characters = list(extract_unicode_characters(title))
    if language.REQUIRES_UNICODE_CHARACTERS and not unicode_characters:
        return False

    if language.FORBIDS_UNICODE_CHARACTERS and unicode_characters:
        return False

    # not sure but all titles I found so far have a clear character set, not shared
    return all([np.any((language.UNICODE_CHARACTER_LOWERS <= int(unichar)) &
                       (int(unichar) <= language.UNICODE_CHARACTER_UPPERS)) for unichar in unicode_characters])
