#!/usr/bin/env python3
"""
Class for testing Trie class
"""
import unittest
from src.trie import Trie
# from src.errors import SearchMiss
# import treevizer


class TestTrieExtra(unittest.TestCase):
    """
    Test class
    """
    def setUp(self):
        """
        Creates an empty instance of Trie class and one
        that is loaded with data from file. Also creates a
        Python list from file with words only
        """
        self.empty_trie = Trie() # Arrange
        self.full_trie = Trie.create_from_file("frequency.txt") # Arrange

    def test_prefix_search_not_ok(self):
        """
        Tests that empty list is returned if there is no match on prefix
        """
        self.assertEqual(self.full_trie.prefix_search("dapt"), []) # Act + Assert


    def test_prefix_is_a_word_ok(self):
        """
        Checks that prefix is included when prefix is a word
        """
        found_prefixes = self.full_trie.prefix_search("adapt")
        correct_list = [('adapted',15157.3), ('adaptation',3707.25), ('adapt',2986.53),
        ('adaptable',469.933),('adapts',422.465),('adaptive',302.213),('adapter',129.746),
        ('adaption',49.0503)]
        self.assertEqual(found_prefixes, correct_list)

    def test_prefix_not_ok(self):
        """
        Tests that mid-part of word is not interpreted as prefix
        """
        self.empty_trie.add_word("jul") # Arrange
        self.empty_trie.add_word("julklapp") # Arrange
        self.empty_trie.add_word("julafton") # Arrange
        self.empty_trie.add_word("jultomte") # Arrange
        found_prefixes = self.empty_trie.prefix_search("klapp") # Act
        self.assertEqual(found_prefixes, []) # Assert

    def test_prefixlimit_ten_ok(self):
        """
        Tests that the search is limited to 10 with top frequency
        """
        correct_list = [('about',1414687),('after',978575),('again',745230),
        ('away',673810),('also',608042),('against',569459),('another',533985),
        ('always',495834),('asked',420044),('among',387549)]
        found_prefixes = self.full_trie.prefix_search("a") # Act
        self.assertEqual(found_prefixes, correct_list) # Assert

    def test_prefixlimit_ten_prefix_is_word_ok(self):
        """
        Tests that the search is limited to 10 with top frequency
        and that word that in itself corresponds to prefix also is included since it has
        the highest frequency
        """
        correct_list = [('band',39397.7),('bands',15567.9),	('bandage',3349.66),
        ('bandit',1537.96),	('bandana',236.549),('bandwidth',69.6198),
        ('bandicoot',53.006),('banderole',45.0946),('bandoleer',34.8099),('bandog',26.8985)]
        found_prefixes = self.full_trie.prefix_search("band") # Act
        self.assertEqual(found_prefixes, correct_list) # Assert

    def test_prefix_emtpystring_not_ok (self):
        """
        Tests that empty string is retruend when searching for empty string
        """
        self.assertEqual(self.full_trie.prefix_search(""), []) # Act and Assert


    def test_correct_spelling_ok(self):
        """
        tests correct spelling, only words with same last letter and at moste two
        differing letters ina  row should be included
        """
        word_suggestions = self.full_trie.correct_spelling("broan")
        correct_list = ['arian','aryan','blown','brown','croon','crown','drown',
        'frown','groan','groin','grown','organ','urban']
        self.assertEqual(word_suggestions, correct_list)

    def test_correct_spelling_last_char_not_ok(self):
        """
        Checks that correct_spelling returns an empty list if the last letter is
        wrong.
        """
        custom_list = ["anas", "apas", "atas", "amas", "aras", "aza", "aman"] # Arrange
        for word in custom_list:
            self.empty_trie.add_word(word) # Arrange
        self.assertEqual(self.empty_trie.correct_spelling("amal"), []) # Act + Assert


    def test_correct_spelling_correct_word_only_ok(self):
        """
        Checks that correct_spelling returns an a list with only correct word
        """
        custom_list = ["beat", "heat", "beet", "belt", "debt", "boot"] # Arrange
        for word in custom_list:
            self.empty_trie.add_word(word) # Arrange
        self.assertEqual(self.empty_trie.correct_spelling("beet"), ["beet"]) # Act + Assert

    def test_correct_spelling_empty_string_not_ok(self):
        """
        Checks that correct_spelling returns an empty list when searching for empty string
        """
        self.assertEqual(self.empty_trie.correct_spelling(""), []) # Act + Assert

    def test_suffix_is_a_word_ok(self):
        """
        Tests that suffix is included in list if it's a word
        """
        suffix_suggestions = self.full_trie.suffix_search("arts")
        correct_list = ['arts','carts','charts','darts','farts','hearts','parts',
        'tarts','warts']
        self.assertEqual(suffix_suggestions, correct_list)

    def test_second_suffix_is_a_word_ok(self):
        """
        Tests that suffix is included in list if it's a word
        """
        suffix_suggestions = self.full_trie.suffix_search("list")
        correct_list = ['annalist',	'blacklist','capitalist','checklist','cyclist',
        'enlist','evangelist','fabulist','fatalist','funambulist','herbalist',
        'idealist','imperialist','journalist','list','monopolist',
        'nationalist','naturalist','noctambulist','novelist','oculist',
        'orientalist','pugilist','realist','royalist','sciolist','socialist',
        'somnambulist','specialist','tricyclist','vocalist']
        self.assertEqual(suffix_suggestions, correct_list)

    def test_suffix_not_ok(self):
        """
        Tests that empty list is returned if no wors with suffix are
        found
        """
        suffix_suggestions = self.full_trie.suffix_search("hfgj")
        self.assertEqual(suffix_suggestions, [])

    def test_contains_ok(self):
        """
        Tests contain method by checking if the Trie contains a
        word that is in Trie
        """
        self.empty_trie.add_word("hej") # Act
        self.empty_trie.add_word("soppa") # Act
        self.empty_trie.add_word("dator") # Act
        self.assertIn("dator", self.empty_trie) # Act + Assert


    def tearDown(self):
        """
        Removes dependencies after test
        """
        self.empty_trie = None
        self.full_trie = None
