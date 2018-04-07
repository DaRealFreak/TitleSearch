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
    def get_similar_titles(title: str) -> list:
        """Main function for extracting alternate titles

        :type title: str
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
    def get_alternative_titles(title: str = '', link: str = '') -> dict:
        """Get alternative titles for the given title. Preferring link over title argument

        :type title: str
        :type link: str
        :return:
        """
        if title and not link:
            link = MyAnimeList.get_similar_titles(title)
            if link:
                link = link[0]['link']
            else:
                return MyAnimeList.group_titles(title, None)

        link = requests.get(url=link)
        soup = Soup(link.text, 'html5lib')

        release_title = soup.find('span', attrs={'itemprop': 'name'})
        if release_title:
            release_title = release_title.text
        else:
            release_title = title if title else ''

        return MyAnimeList.group_titles(release_title=release_title, soup=soup)

    @staticmethod
    def group_titles(release_title: str, soup) -> dict:
        """Extract and group the titles of the bs4 Tag to their respective language

        :type release_title: str
        :type soup: bs4.element.Tag|None
        :return:
        """
        grouped_titles = {}
        for language in MyAnimeList.KNOWN_LANGUAGES:
            grouped_titles[language.__name__.lower()] = []

        grouped_titles['english'] = [release_title]

        if soup:
            for search_result in soup.find_all('div', attrs={'class': 'spaceit_pad'}):  # type:
                category = search_result.find('span', attrs={'class': 'dark_text'})
                if category:
                    value = "".join(
                        [t for t in search_result.contents if isinstance(t, bs4.element.NavigableString)]).strip()
                    if category.text.strip() == 'Synonyms:':
                        for synonym in value.split(', '):
                            grouped_titles[MyAnimeList.MAPPING[category.text]].append(synonym)
                    else:
                        if category.text.strip() in MyAnimeList.MAPPING:
                            grouped_titles[MyAnimeList.MAPPING[category.text.strip()]].append(value)

        return grouped_titles
