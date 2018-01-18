#!/usr/local/bin/python
# coding: utf-8
import abc


class LanguageTemplate:
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def unicode_character_lowers(self):
        pass

    @property
    @abc.abstractmethod
    def unicode_character_uppers(self):
        pass

    @property
    @abc.abstractmethod
    def requires_unicode_characters(self):
        pass

    @property
    @abc.abstractmethod
    def forbids_unicode_characters(self):
        pass
