#!/usr/local/bin/python
# coding: utf-8
import requests
from bs4 import BeautifulSoup as Soup

from titlesearch.language.language_settings import *


class MyAnimeList(object):
    """Module for extracting alternative language titles for titles from mangaupdates.com"""

    SEARCH_URL = 'https://vndb.org/v/all'
    KNOWN_LANGUAGES = [English, Japanese, Korean]
    ADDED_KEYWORDS = [' (Novel)']

    @staticmethod
    def get_similar_titles(title):
        """Main function for extracting alternate titles

        :param title:
        :return:
        """
        payload = {
            'sq': title
        }

        link = requests.get(url=MyAnimeList.SEARCH_URL, params=payload)
        soup = Soup(link.text, 'html.parser')

    @staticmethod
    def get_alternative_titles(title='', link=''):
        """Get alternative titles for the given title. Preferring link over title argument

        :param title:
        :param link:
        :return:
        """
        if title and not link:
            link = MyAnimeList.get_similar_titles(title)[0]['link']

        link = requests.get(url=link)

        # html.parser can't handle <br> tags instead of <br/> tags and will append all titles as child
        # to the previous title, html5lib is slower but works properly
        soup = Soup(link.text, 'html5lib')

    @staticmethod
    def clean_title(title):
        """Strip title from leftover spaces and remove keywords added by VisualNovelDatabase

        :param title:
        :return:
        """
        title = title.strip()
        for keyword in MyAnimeList.ADDED_KEYWORDS:
            title = title.replace(keyword, '')
        return title
