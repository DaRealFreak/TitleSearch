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
    return light_novel_results


def get_alternative_titles(title=''):
    """Search the 3 different modules for an alternative title of the given title and return a
    dictionary split into the different languages

    :param title:
    :return:
    """
    light_novel_results = BakaUpdates.get_alternative_titles(title=title)
    visual_novel_results = VisualNovelDatabase.get_alternative_titles(title=title)
    anime_results = MyAnimeList.get_alternative_titles(title=title)
    return light_novel_results
