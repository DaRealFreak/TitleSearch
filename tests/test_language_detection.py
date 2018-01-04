#!/usr/local/bin/python
# coding: utf-8
import unittest

from bakaupdates.language.detection import matches_language
from bakaupdates.language.language_settings import *


class TestLanguageDetection(unittest.TestCase):
    titles = [
        'Tate no Yuusha no Nariagari',
        'Tate no Yūsha no Nariagari',
        '盾の勇者の成り上がり',
        '방패 용사 성공담',
        'The Rising of the Shield Hero'
    ]

    EXPECTED_RESULTS_ENGLISH = [
        True,
        False,
        False,
        False,
        True
    ]

    EXPECTED_RESULTS_KOREAN = [
        False,
        False,
        False,
        True,
        False
    ]

    EXPECTED_RESULTS_JAPANESE = [
        False,
        False,
        True,
        False,
        False
    ]

    def test_korean_results(self):
        """Test the titles with the korean language configuration"""
        results = []
        for title in self.titles:
            results.append(matches_language(title, Korean))

        self.assertEqual(self.EXPECTED_RESULTS_KOREAN, results)

    def test_japanese_detection(self):
        """Test the titles with the japanese language configuration"""
        results = []
        for title in self.titles:
            results.append(matches_language(title, Japanese))

        self.assertEqual(self.EXPECTED_RESULTS_JAPANESE, results)

    def test_english_detection(self):
        """Test the titles with the english language configuration"""
        results = []
        for title in self.titles:
            results.append(matches_language(title, English))

        self.assertEqual(self.EXPECTED_RESULTS_ENGLISH, results)


suite = unittest.TestLoader().loadTestsFromTestCase(TestLanguageDetection)
unittest.TextTestRunner(verbosity=2).run(suite)
