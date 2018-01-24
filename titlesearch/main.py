#!/usr/local/bin/python
# coding: utf-8
from titlesearch.bakaupdates import BakaUpdates
from titlesearch.mal import MyAnimeList
from titlesearch.vndb import VisualNovelDatabase


def get_similar_titles(title):
    """search the 3 different modules for a similar title and return a list sorted by similarity

    :param title:
    :return:
    """
    light_novel_results = BakaUpdates.get_similar_titles(title)
    visual_novel_results = VisualNovelDatabase.get_similar_titles(title)
    anime_results = MyAnimeList.get_similar_titles(title)

    results = []
    passed_titles = []

    for result_list in (light_novel_results, visual_novel_results, anime_results):
        for result in result_list:
            if result['title'] in passed_titles:
                results[passed_titles.index(result['title'])]['links'].append(result['link'])
            else:
                results.append({
                    'title': result['title'],
                    'links': [result['link']],
                    'similarity': result['similarity']
                })
                passed_titles.append(result['title'])

    results.sort(key=lambda item: item['similarity'], reverse=True)
    return results


def get_alternative_titles(title=''):
    """Search the 3 different modules for an alternative title of the given title and return a
    dictionary split into the different languages

    :param title:
    :return:
    """
    light_novel_results = BakaUpdates.get_alternative_titles(title=title)
    visual_novel_results = VisualNovelDatabase.get_alternative_titles(title=title)
    anime_results = MyAnimeList.get_alternative_titles(title=title)

    alternative_titles = {}

    for result_list in (light_novel_results, visual_novel_results, anime_results):
        for language in result_list:
            if not result_list[language]:
                continue

            for title in result_list[language]:
                if language not in alternative_titles:
                    alternative_titles[language] = [title]
                    continue

                if title not in alternative_titles[language]:
                    alternative_titles[language].append(title)

    return alternative_titles
