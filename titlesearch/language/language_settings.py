#!/usr/local/bin/python
# coding: utf-8
"""
configuration for the different languages, mostly viable for asian languages since they have
big differences between the used characters.
Unicode ranges mostly taken from here: http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
"""

import numpy as np

from titlesearch.language import LanguageTemplate


class English(LanguageTemplate):
    unicode_character_lowers = np.array([])
    unicode_character_uppers = np.array([])

    requires_unicode_characters = False
    forbids_unicode_characters = True


class Korean(LanguageTemplate):
    """
    Hangul Syllables (AC00-D7A3) which corresponds to (가-힣)
    Hangul Jamo (1100–11FF)
    Hangul Compatibility Jamo (3130-318F)
    Hangul Jamo Extended-A (A960-A97F)
    Hangul Jamo Extended-B (D7B0-D7FF)
    """
    unicode_character_lowers = np.array([0xAC00, 0x1100, 0x3130, 0xA960, 0xD7B0])
    unicode_character_uppers = np.array([0xD7A3, 0x11FF, 0x318F, 0xA97F, 0xD7FF])

    requires_unicode_characters = True
    forbids_unicode_characters = False


class Japanese(LanguageTemplate):
    """
    JAPANESE_PUNCTUATION=(0x3000, 0x3F)
    JAPANESE_HIRAGANA=(0x3040, 0x5f)
    JAPANESE_KATAKANA=(0x30A0, 0x5f)
    JAPANESE_ROMAN_HALF_WIDTH_KATAKANA=(0xFF00, 0xEF)
    JAPANESE_KANJI=(0x4e00, 0x9FAF)
    JAPANESE_KANJI_RARE=(0x3400, 0x19BF)
    """
    unicode_character_lowers = np.array([0x3000, 0x3040, 0x30a0, 0xff00, 0x4e00, 0x3400])
    unicode_character_uppers = np.array([0x303f, 0x309f, 0x30ff, 0xffef, 0x9FAF, 0x4dbf])

    requires_unicode_characters = True
    forbids_unicode_characters = False
