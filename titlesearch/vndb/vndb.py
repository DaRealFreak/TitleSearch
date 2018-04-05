#!/usr/local/bin/python
# coding: utf-8

import re

import jellyfish
import requests
from bs4 import BeautifulSoup as Soup

from titlesearch.language.detection import matches_language
from titlesearch.language.language_settings import *


class VisualNovelDatabase(object):
    """Module for extracting alternative language titles for titles from https://vndb.org"""

    ROOT_URL = 'https://vndb.org/'
    SEARCH_URL = 'https://vndb.org/v/all'
    KNOWN_LANGUAGES = [English, Japanese, Korean]

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

        link = requests.get(url=VisualNovelDatabase.SEARCH_URL, params=payload)
        # use html5lib here to generate a tbody tag from the table(not generated with html.parser)
        soup = Soup(link.text, 'html5lib')

        # if the match is above a certain percentage we won't get to the search result page but to the
        # detail page of the search result so we won't get more than 1 result
        current_url = soup.select_one('meta[property="og:url"]')
        # not set apparently in the search result page
        if current_url and re.match('{0:s}v\d+'.format(VisualNovelDatabase.ROOT_URL), current_url['content']):
            return [{
                'title': title,
                'link': current_url['content'],
                'similarity': 1.00
            }]

        title_links = soup.select('tbody td a')
        for search_result in title_links:
            results.append({
                'title': search_result['title'],
                'link': VisualNovelDatabase.ROOT_URL + search_result['href'],
                'similarity': jellyfish.jaro_distance(search_result['title'].lower(), title.lower())
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
            link = VisualNovelDatabase.get_similar_titles(title)
            if link:
                link = link[0]['link']
            else:
                return VisualNovelDatabase.group_titles(title, [])

        link = requests.get(url=link)

        result_data = VisualNovelDatabase.parse_results(link.text)

        alternative_titles = []
        if 'Aliases' in result_data:
            for alternative_title in result_data['Aliases'].split(', '):
                alternative_titles.append(alternative_title)
        if 'Original title' in result_data:
            alternative_titles.append(result_data['Original title'])

        return VisualNovelDatabase.group_titles(release_title=result_data['Title'],
                                                alternative_titles=alternative_titles)

    @staticmethod
    def parse_results(html_content: str) -> dict:
        """Parse the result table of the HTML content into a dictionary

        :type html_content: str
        :return:
        """
        soup = Soup(html_content, 'html.parser')
        result_data = {}

        #
        table_body = soup.select_one('div.vndetails table')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols if ele.text.strip()]
            if cols[1:]:
                result_data[cols[0]] = cols[1]

        return result_data

    @staticmethod
    def group_titles(release_title: str, alternative_titles: list) -> dict:
        """Iterate through the supported languages and group the titles according to the detected languages

        :type release_title: str
        :type alternative_titles: list
        :return:
        """
        grouped_titles = {}
        for language in VisualNovelDatabase.KNOWN_LANGUAGES:
            grouped_titles[language.__name__.lower()] = []

        grouped_titles['english'] = [release_title]

        for title in alternative_titles:
            for language in VisualNovelDatabase.KNOWN_LANGUAGES:
                if matches_language(title, language) and title not in grouped_titles[language.__name__.lower()]:
                    grouped_titles[language.__name__.lower()].append(title)
                    continue

        return grouped_titles
