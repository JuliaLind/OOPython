#!/usr/bin/env python3
"""
Class for testing Trie class
"""
import unittest
from src.trie import Trie
from src.errors import SearchMiss
# import treevizer


class TestTrie(unittest.TestCase):
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

        self.words_only_full_list = [] # Arrange
        with open("frequency.txt", "r", encoding="utf-8")as fhand:
            content = fhand.readlines()
        for line in content:
            line = line.split()
            self.words_only_full_list.append(line[0]) # Arrange
        self.words_only_full_list.sort() # Arrange

    def _get_false_leafs(self, node):
        my_list = []
        if not node.children and not node.stop:
            my_list.append(node.value)
        elif node.children:
            for child in node.children.values():
                my_list += self._get_false_leafs(child)
        return my_list

    def test_word_count(self):
        """
        Checks that word_count method returns correct number
        """
        self.assertEqual(self.full_trie.word_count(), len(self.words_only_full_list)) # Act + Assert

    def test_add_word_ok(self):
        """
        Adds a word to an empty Trie. Checks that
        the word is in Trie
        """
        self.empty_trie.add_word("hej") # Act
        self.assertIn("hej", self.empty_trie) # Assert

    def test_add_shorter_word_in_word_ok(self):
        """
        Adds a long word and then a short word that is also a prefix
        to the long word. Checks that both have been marked as words
        """
        self.empty_trie.add_word("julafton") # Act
        self.empty_trie.add_word("jul") # Act
        self.assertIn("jul", self.empty_trie) # Assert
        self.assertIn("julafton", self.empty_trie) # Assert



    def test_add_longer_word_in_word_ok(self):
        """
        Adds a short word and then a long word for which
        the short word is prefix. Checks that both have been marked
        as words
        """
        self.empty_trie.add_word("jul") # Act
        self.empty_trie.add_word("julafton") # Act

        self.assertIn("jul", self.empty_trie) # Assert
        self.assertIn("julafton", self.empty_trie) # Assert

    def test_load_from_file_ok(self):
        """
        Tests that words from file have been loaded
        by searching for the first word, last word and middle
        word in the file
        """
        self.assertIn("that", self.full_trie) # Assert
        self.assertIn("turn", self.full_trie) # Assert
        self.assertIn("zoetrope", self.full_trie) # Assert

    def test_all_words_ok(self):
        """
        Tests that all_words method returns all words from the file
        """
        self.assertEqual(self.full_trie.all_words(), self.words_only_full_list) # Act + Assert

    def test_find_ok(self):
        """
        Tests the find method by checking if the Trie contains a
        word that is in Trie. Should return bool True
        """
        self.assertTrue(self.full_trie.find("smarmy")) # Act + Assert

    def test_find_searchmiss_not_ok(self):
        """
        Searches for a word in a non-empty Trie,
        that is not in the trie. The word is a prefix to a
        real word. Checks that the
        SearchMiss exception is raised
        """
        with self.assertRaises(SearchMiss) as _:
            self.full_trie.find("sycami") # Act + Assert

    def test_find_emptystring_not_ok(self):
        """
        Searches for a word in a non-empty Trie,
        that is not in the trie. The word is a prefix to a
        real word. Checks that the
        SearchMiss exception is raised
        """
        with self.assertRaises(SearchMiss) as _:
            self.full_trie.find("") # Act + Assert

    def test_empty_trie_find_searchmiss_not_ok(self):
        """
        Searches for a word in an empty Trie. Checks that the
        SearchMiss exception is raised"
        """
        with self.assertRaises(SearchMiss) as _:
            self.empty_trie.find("hello") # Act + Assert

    def test_remove_ok(self):
        """
        Tests the remove method by removing the words that were
        added first, last and in the middle.
        Checks that each of the words is not on the trie.
        Also checks that all the other words are still in the Trie
        """
        self.words_only_full_list.remove("that") # Arrange
        self.words_only_full_list.remove("turn") # Arrange
        self.words_only_full_list.remove("zoetrope") # Arrange
        self.full_trie.remove("that") # Act
        self.full_trie.remove("turn") # Act
        self.full_trie.remove("zoetrope") # Act

        self.assertNotIn("that", self.full_trie) # Assert
        self.assertNotIn("turn", self.full_trie) # Assert
        self.assertNotIn("zoetrope", self.full_trie) # Assert
        self.assertEqual(self.full_trie.all_words(), self.words_only_full_list) # Assert

    def test_remove_not_ok(self):
        """
        Tests that exception is lifted if attempting to remove a letter combination
        that is a partial of a word in the trie but not a word of its own
        """
        with self.assertRaises(SearchMiss) as _:
            self.full_trie.remove("aarg") # Act + Assert
        self.assertIn("aargau", self.full_trie)

    def test_remove_empty_string_not_ok(self):
        """
        Tests that exception is lifted if attempting to remove a letter combination
        that is a partial of a word in the trie but not a word of its own
        """
        with self.assertRaises(SearchMiss) as _:
            self.full_trie.remove("") # Act + Assert
        self.assertIn("aargau", self.full_trie)

    def test_remove_shorter_word_in_word_ok(self):
        """
        Adds two words of which one is also prefix to the other.
        Removes the shorter word and checks if the longer word is
        still in trie
        """
        self.empty_trie.add_word("jul") # Arrange
        self.empty_trie.add_word("julafton") # Arrange
        self.empty_trie.remove("jul") # Act
        self.assertIn("julafton", self.empty_trie) # Assert
        self.assertNotIn("jul", self.empty_trie) # Assert


    def test_remove_longer_word_in_word_ok(self):
        """
        Adds two words of which one is also prefix to the other.
        Removes the longer word and checks if the shorter word is
        still in trie and that the longer word has been removed properly by checking for
        false leafs
        """
        self.empty_trie.add_word("jul") # Arrange
        self.empty_trie.add_word("julafton") # Arrange
        self.empty_trie.remove("julafton") # Act

        # treevizer.to_png(self.empty_trie.root, "trie", "trie.tree", png_path="trie.png")

        self.assertIn("jul", self.empty_trie) # Assert
        self.assertNotIn("julafton", self.empty_trie) # Assert
        test_list = self._get_false_leafs(self.empty_trie.root)
        self.assertEqual(test_list, [])

    def tearDown(self):
        """
        Removes dependencies after test
        """
        self.empty_trie = None
        self.full_trie = None
        self.words_only_full_list = None
