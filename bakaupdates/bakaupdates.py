#!/usr/local/bin/python
# coding: utf-8
import difflib
import operator
import re

import numpy as np
import requests
from bs4 import BeautifulSoup as Soup


class BakaUpdates(object):
    """Module for extracting alternative language titles for titles from mangaupdates.com"""

    SEARCH_URL = 'https://www.mangaupdates.com/series.html'

    def __init__(self):
        pass

    def search_titles(self, title):
        """Main function for extracting alternate titles

        :param title:
        :return:
        """
        payload = {
            'stype': 'title',
            'search': 'Tate no Yuusha no Nariagari'
        }

        link = requests.post(url=self.SEARCH_URL, params=payload)
        soup = Soup(link.text, 'html.parser')

        print(soup.prettify())
        exit(1)
        results = []
        matches = []
        for url, res_title in results:
            match = difflib.SequenceMatcher(None, res_title.lower(), title.lower()).ratio()
            matches.append((res_title, url, match))
        matches.sort(key=operator.itemgetter(2), reverse=True)

    def open_title(self, titles):
        """Parse the page content of the best matched title

        :param titles:
        :return:
        """
        jp_raw_titles = self.extract_japanese_titles(titles)
        kr_raw_titles = self.extract_korean_titles(titles)
        en_titles = [t for t in titles if not bool(re.search('&#\d{4,6};', t)) and len(t) > 0]
        jp_titles = [self.assemble_unicode_title(title) for title in jp_raw_titles]
        kr_titles = [self.assemble_unicode_title(title) for title in kr_raw_titles]

    def extract_japanese_titles(self, titles):
        """Extract the japanese titles from the page content based on the used characters

        :param titles:
        :return:
        """
        return [title for title in titles if
                bool(re.search('&#\d{4,6};', title)) and self.determine_japanese_title(title)]

    def extract_korean_titles(self, titles):
        """Extract the korean titles from the page content based on the used characters

        :param titles:
        :return:
        """
        return [title for title in titles if
                bool(re.search('&#\d{4,6};', title)) and self.determine_korean_title(title)]

    @staticmethod
    def determine_japanese_title(title):
        """Determine based on unicode elements, if the title is japanese.
        JAPANESE_PUNCTUATION=(0x3000, 0x3F)
        JAPANESE_HIRAGANA=(0x3040, 0x5f)
        JAPANESE_KATAKANA=(0x30A0, 0x5f)
        JAPANESE_ROMAN_HALF_WIDTH_KATAKANA=(0xFF00, 0xEF)
        JAPANESE_KANJI=(0x4e00, 0x51AF)
        JAPANESE_KANJI_RARE=(0x3400, 0x19BF)

        :param title:
        :return:
        """
        lows = np.array([0x3000, 0x3040, 0x30a0, 0xff00, 0x4e00, 0x3400])  # the lower bounds
        ups = np.array([0x303f, 0x309f, 0x30ff, 0xffef, 0x51AF, 0x4dbf])  # the upper bounds
        unichars = re.findall('&#([\d]{4,6});', title)
        # any thanks to shared characters with chinese
        return any([np.any((lows <= int(unichar)) & (int(unichar) <= ups)) for unichar in unichars])

    @staticmethod
    def determine_korean_title(title):
        """Determine based on unicode elements, if the title is korean.
        Hangul Syllables (AC00-D7A3) which corresponds to (가-힣)
        Hangul Jamo (1100–11FF)
        Hangul Compatibility Jamo (3130-318F)
        Hangul Jamo Extended-A (A960-A97F)
        Hangul Jamo Extended-B (D7B0-D7FF)

        :param title:
        :return:
        """
        lows = np.array([0xAC00, 0x1100, 0x3130, 0xA960, 0xD7B0])  # the lower bounds
        ups = np.array([0xD7A3, 0x11FF, 0x318F, 0xA97F, 0xD7FF])  # the upper bounds
        unichars = re.findall('&#([\d]{4,6});', title)
        # not sure but all titles I found so far have a clear character set, not shared
        return all([np.any((lows <= int(unichar)) & (int(unichar) <= ups)) for unichar in unichars])

    @staticmethod
    def assemble_unicode_title(title):
        """Replace the stand-in characters from our title with the real characters

        :param title:
        :return:
        """
        unichars = re.findall('&#([\d]{4,6});', title)
        for unichar in unichars:
            title = title.replace('&#{0:s};'.format(unichar), str(chr(int(unichar))))
        return title
