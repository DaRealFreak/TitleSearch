#!/usr/local/bin/python
# coding: utf-8
from bakaupdates.language.detection import matches_language
from bakaupdates.language.language_settings import *

titles = [
    'Tate no Yuusha no Nariagari',
    'Tate no Yūsha no Nariagari',
    '盾の勇者の成り上がり',
    '방패 용사 성공담',
    'The Rising of the Shield Hero'
]

for title in titles:
    print(title)
    print("is korean: " + str(matches_language(title, Korean)))
    print("is japanese: " + str(matches_language(title, Japanese)))
    print("is english: " + str(matches_language(title, English)))
