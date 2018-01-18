#!/usr/local/bin/python
# coding: utf-8
import difflib
import re

import requests
from bs4 import BeautifulSoup as Soup

from titlesearch.language.detection import matches_language
from titlesearch.language.language_settings import *


class BakaUpdates(object):
    """Module for extracting alternative language titles for titles from mangaupdates.com"""

    SEARCH_URL = 'https://www.mangaupdates.com/series.html'
    KNOWN_LANGUAGES = [English, Japanese, Korean]
    ADDED_KEYWORDS = [' (Novel)']

    @staticmethod
    def get_similar_titles(title):
        """Main function for extracting alternate titles

        :param title:
        :return:
        """
        payload = {
            'stype': 'title',
            'search': title
        }

        link = requests.get(url=BakaUpdates.SEARCH_URL, params=payload)
        soup = Soup(link.text, 'html.parser')

        seen_titles = []
        results = []
        for s in soup.find_all('td', attrs={"class": "text pad col1"}):
            search_result = BakaUpdates.clean_title(s.text)
            # I decided to add a seen titles list to prevent duplicate titles in the output.
            # BakaUpdates search returns titles without the added keywords first, so I'll skip the second result
            # which is most likely a novel
            if search_result not in seen_titles:
                results.append({'title': search_result,
                                'link': s.find_next('a', href=True)['href'],
                                'similarity': difflib.SequenceMatcher(None,
                                                                      search_result.lower(),
                                                                      title.lower()).ratio()
                                })
                seen_titles.append(search_result)

        results.sort(key=lambda item: item['similarity'], reverse=True)
        if len(results) < 1:
            return []

        return results

    @staticmethod
    def get_alternative_titles(title='', link=''):
        """Get alternative titles for the given title. Preferring link over title argument

        :param title:
        :param link:
        :return:
        """
        if title and not link:
            link = BakaUpdates.get_similar_titles(title)[0]['link']

        link = requests.get(url=link)

        # html.parser can't handle <br> tags instead of <br/> tags and will append all titles as child
        # to the previous title, html5lib is slower but works properly
        soup = Soup(link.text, 'html5lib')

        release_title = soup.find('span', attrs={'class': ['releasestitle', 'tabletitle']}).text
        associated_names_tag = soup.find('b', string=re.compile("Associated Names"))
        alternative_titles = associated_names_tag.parent.find_next_sibling('div', attrs={'class': 'sContent'})
        for br in alternative_titles.find_all("br"):
            br.replace_with("\n")
        alternative_titles = [BakaUpdates.clean_title(title) for title in alternative_titles.text.split('\n')
                              if title.strip()]

        grouped_titles = {}
        for language in BakaUpdates.KNOWN_LANGUAGES:
            grouped_titles[language.__name__.lower()] = []
        grouped_titles['english'] = [release_title]

        for title in alternative_titles:
            for language in BakaUpdates.KNOWN_LANGUAGES:
                if matches_language(title, language) and title not in grouped_titles[language.__name__.lower()]:
                    grouped_titles[language.__name__.lower()].append(title)
                    continue

        return grouped_titles

    @staticmethod
    def clean_title(title):
        """Strip title from leftover spaces and remove keywords added by BakaUpdates

        :param title:
        :return:
        """
        title = title.strip()
        for keyword in BakaUpdates.ADDED_KEYWORDS:
            title = title.replace(keyword, '')
        return title
