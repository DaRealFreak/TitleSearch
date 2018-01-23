#!/usr/local/bin/python
# coding: utf-8
import difflib
import re

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
    def get_similar_titles(title):
        """Main function for extracting alternate titles

        :param title:
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

        # maincontent > div.mainbox.browse.vnbrowse > table > tbody > tr:nth-child > td.tc1 > a
        title_links = soup.select('tbody td a')
        for search_result in title_links:
            results.append({
                'title': search_result['title'],
                'link': VisualNovelDatabase.ROOT_URL + search_result['href'],
                'similarity': difflib.SequenceMatcher(None, search_result['title'].lower(), title.lower()).ratio()
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
        for language in VisualNovelDatabase.KNOWN_LANGUAGES:
            grouped_titles[language.__name__.lower()] = []

        if title and not link:
            link = VisualNovelDatabase.get_similar_titles(title)
            if link:
                link = link[0]['link']
            else:
                return grouped_titles

        link = requests.get(url=link)

        soup = Soup(link.text, 'html.parser')

        result_data = {}

        # parse the result table into a dictionary
        table_body = soup.select_one('div.vndetails table')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols if ele.text.strip()]
            if cols[1:]:
                result_data[cols[0]] = cols[1]

        grouped_titles['english'] = [result_data['Title']]

        alternative_titles = []
        if 'Aliases' in result_data:
            for alternative_title in result_data['Aliases'].split(', '):
                alternative_titles.append(alternative_title)
        if 'Original title' in result_data:
            alternative_titles.append(result_data['Original title'])

        for title in alternative_titles:
            for language in VisualNovelDatabase.KNOWN_LANGUAGES:
                if matches_language(title, language) and title not in grouped_titles[language.__name__.lower()]:
                    grouped_titles[language.__name__.lower()].append(title)
                    continue

        return grouped_titles
