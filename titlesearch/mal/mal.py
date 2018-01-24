#!/usr/local/bin/python
# coding: utf-8
import re

import bs4
import jellyfish
import requests
from bs4 import BeautifulSoup as Soup

from titlesearch.language.language_settings import *


class MyAnimeList(object):
    """Module for extracting alternative language titles for titles from mangaupdates.com"""

    SEARCH_URL = 'https://myanimelist.net/search/all'
    KNOWN_LANGUAGES = [English, Japanese]
    ADDED_KEYWORDS = [' (Novel)']
    MAPPING = {
        'English:': 'english',
        'Synonyms:': 'english',
        'Japanese:': 'japanese'
    }

    @staticmethod
    def get_similar_titles(title):
        """Main function for extracting alternate titles

        :param title:
        :return:
        """
        payload = {
            'q': title
        }

        results = []

        link = requests.get(url=MyAnimeList.SEARCH_URL, params=payload)
        # html5lib parser since html.parser will fail at the content-left div already
        soup = Soup(link.text, 'html5lib')
        for search_result in soup.select('div.content-left div.list.di-t.w100 a.hoverinfo_trigger'):
            search_group = re.search('/anime/|/manga/', search_result['href'])
            if search_result.text.strip() and search_group:
                results.append({
                    'title': search_result.text.strip(),
                    'link': search_result['href'],
                    'similarity': jellyfish.jaro_distance(search_result.text.strip().lower(), title.lower())
                })
        results.sort(key=lambda item: item['similarity'], reverse=True)
        return results

    @staticmethod
    def get_alternative_titles(title='', link=''):
        """Get alternative titles for the given title. Preferring link over title argument

        :param title:
        :param link:
        :return:
        """
        grouped_titles = {}
        for language in MyAnimeList.KNOWN_LANGUAGES:
            grouped_titles[language.__name__.lower()] = []

        if title and not link:
            link = MyAnimeList.get_similar_titles(title)
            if link:
                link = link[0]['link']
            else:
                return grouped_titles

        link = requests.get(url=link)

        soup = Soup(link.text, 'html5lib')

        release_title = soup.find('span', attrs={'itemprop': 'name'})
        """
        recreating an array vs appending values to an array

        a = []; a = [1]
        runtime:
            >> timeit.timeit('a = []; a = [1]', number=10**7)
            >> 0.5276432445431638

        1            0 BUILD_LIST               0
                     2 STORE_NAME               0 (a)
                     4 LOAD_CONST               0 (1)
                     6 BUILD_LIST               1
                     8 STORE_NAME               0 (a)
                     10 LOAD_CONST              1 (None)
                     12 RETURN_VALUE

        a = []; a.append(1)
        runtime:
            >> timeit.timeit('a = []; a.append(1)', number=10**7)
            >> 0.99629117289982

        1           0 BUILD_LIST               0
                    2 STORE_NAME               0 (a)
                    4 LOAD_NAME                0 (a)
                    6 LOAD_ATTR                1 (append)
                    8 LOAD_CONST               0 (1)
                    10 CALL_FUNCTION           1
                    12 POP_TOP
                    14 LOAD_CONST              1 (None)
                    16 RETURN_VALUE
        """
        grouped_titles['english'] = [release_title.text]

        for search_result in soup.find_all('div', attrs={'class': 'spaceit_pad'}):  # type: bs4.element.Tag
            category = search_result.find('span', attrs={'class': 'dark_text'})
            if category:
                value = "".join([t for t in search_result.contents if type(t) == bs4.element.NavigableString]).strip()
                if category.text.strip() == 'Synonyms:':
                    for synonym in value.split(', '):
                        grouped_titles[MyAnimeList.MAPPING[category.text]].append(synonym)
                else:
                    if category.text.strip() in MyAnimeList.MAPPING:
                        grouped_titles[MyAnimeList.MAPPING[category.text.strip()]].append(value)

        return grouped_titles
