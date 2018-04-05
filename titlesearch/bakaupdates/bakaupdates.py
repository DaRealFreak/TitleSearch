#!/usr/local/bin/python
# coding: utf-8

import re
from typing import Tuple

import jellyfish
import requests
from bs4 import BeautifulSoup as Soup

from titlesearch.language.detection import matches_language
from titlesearch.language.language_settings import *


class BakaUpdates(object):
    """Module for extracting alternative language titles for titles from https://www.mangaupdates.com"""

    SEARCH_URL = 'https://www.mangaupdates.com/series.html'
    KNOWN_LANGUAGES = [English, Japanese, Korean]
    ADDED_KEYWORDS = [' (Novel)']

    @staticmethod
    def get_similar_titles(title: str) -> list:
        """Main function for extracting alternate titles

        :type title: str
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
                results.append({
                    'title': search_result,
                    'link': s.find_next('a', href=True)['href'],
                    'similarity': jellyfish.jaro_distance(search_result.lower(), title.lower())
                })
                seen_titles.append(search_result)

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
            link = BakaUpdates.get_similar_titles(title)
            if link:
                link = link[0]['link']
            else:
                return BakaUpdates.group_titles(title, [])

        link = requests.get(url=link)
        release_title, alternative_titles = BakaUpdates.extract_titles(link.text)
        return BakaUpdates.group_titles(release_title, alternative_titles)

    @staticmethod
    def extract_titles(html_content: str) -> Tuple[str, list]:
        """Extract the titles from the HTML DOM tree

        :type html_content: str
        :return:
        """
        # html.parser can't handle <br> tags instead of <br/> tags and will append all titles as child
        # to the previous title, html5lib is slower but works properly
        soup = Soup(html_content, 'html5lib')

        release_title = soup.find('span', attrs={'class': ['releasestitle', 'tabletitle']}).text
        associated_names_tag = soup.find('b', string=re.compile("Associated Names"))
        alternative_titles = associated_names_tag.parent.find_next_sibling('div', attrs={'class': 'sContent'})
        for br in alternative_titles.find_all("br"):
            br.replace_with("\n")
        alternative_titles = [BakaUpdates.clean_title(title) for title in alternative_titles.text.split('\n')
                              if title.strip()]

        return release_title, alternative_titles

    @staticmethod
    def group_titles(release_title: str, alternative_titles: list) -> dict:
        """Iterate through the supported languages and group the titles according to the detected languages

        :type release_title: str
        :type alternative_titles: str
        :return:
        """
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
    def clean_title(title: str) -> str:
        """Strip title from leftover spaces and remove keywords added by BakaUpdates

        :type title: str
        :return:
        """
        title = title.strip()
        for keyword in BakaUpdates.ADDED_KEYWORDS:
            title = title.replace(keyword, '')
        return title
