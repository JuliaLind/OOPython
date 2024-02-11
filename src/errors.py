#!/usr/bin/env python3
"""
Exception classes
"""

class SpellcheckExceptions(Exception):
    """
    Base class for exceptions in Spellchecker program
    """

class SearchMiss(SpellcheckExceptions):
    """
    Raised when the word is not foud in the Trie object
    """
