#!/usr/bin/python
# -*- coding: utf-8 -*-
from bakaupdates import BakaUpdates

if __name__ == '__main__':
    bu = BakaUpdates()
    titles = bu.search_titles("Tate no Yuusha no Nariagari")
    for language in titles:
        for title in titles[language]:
            try:
                print("[{0:s}]: {1:s}".format(language, title))
            except UnicodeEncodeError:
                print("[{0:s}]: lenghth: {1:d}".format(language, len(title)))