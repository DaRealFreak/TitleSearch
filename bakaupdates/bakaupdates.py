#!/usr/local/bin/python
# coding: utf-8
import difflib
import re

import requests
from bs4 import BeautifulSoup as Soup

from bakaupdates.exceptions import *
from bakaupdates.language.detection import matches_language
from bakaupdates.language.language_settings import *


class BakaUpdates(object):
    """Module for extracting alternative language titles for titles from mangaupdates.com"""

    SEARCH_URL = 'https://www.mangaupdates.com/series.html'

    def __init__(self):
        pass

    def get_similar_titles(self, title):
        """Main function for extracting alternate titles

        :param title:
        :return:
        """
        payload = {
            'stype': 'title',
            'search': title
        }

        link = requests.post(url=self.SEARCH_URL, params=payload)
        soup = Soup(link.text, 'html.parser')

        results = []
        for s in soup.find_all('td', attrs={"class": "text pad col1"}):
            results.append({'title': s.text,
                            'link': s.find_next('a', href=True)['href'],
                            'similarity': difflib.SequenceMatcher(None, s.text.lower(), title.lower()).ratio()
                            })

        results.sort(key=lambda item: item['similarity'], reverse=True)
        if len(results) < 1:
            raise NoTitlesFoundException("No titles found")

        return results

    def get_alternative_titles(self, title='', link=''):
        """Get alternative titles for the given title. Preferring link over title argument

        :param title:
        :param link:
        :return:
        """
        if title and not link:
            link = self.get_similar_titles(title)[0]['link']

        link = requests.post(url=link)

        # html.parser can't handle <br> tags instead of <br/> tags and will append all titles as child
        # to the previous title, html5lib is slower but works properly
        soup = Soup(link.text, 'html5lib')
        associated_names_tag = soup.find('b', string=re.compile("Associated Names"))
        alternative_titles = associated_names_tag.parent.find_next_sibling('div', attrs={'class': 'sContent'})
        for br in alternative_titles.find_all("br"):
            br.replace_with("\n")
        alternative_titles = [title.strip() for title in alternative_titles.text.split('\n') if title.strip()]

        grouped_titles = {
            'english': [],
            'korean': [],
            'japanese': []
        }
        for title in alternative_titles:
            if matches_language(title, English):
                grouped_titles['english'].append(title)
                continue
            if matches_language(title, Korean):
                grouped_titles['korean'].append(title)
                continue
            if matches_language(title, Japanese):
                grouped_titles['japanese'].append(title)
                continue
        return grouped_titles
