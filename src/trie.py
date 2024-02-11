#!/usr/bin/env python3
"""
Trie class
"""

from src.node import Node
from src.errors import SearchMiss
from src.sort import sort_on_freq
# import treevizer

class Trie:
    """
    Trie class
    """
    def __init__(self):
        """
        Constructor.
        """
        self.root = Node()

    def _add_word(self, node, word, frequency=1):
        """
        Recursive method for adding a word
        """
        if len(word) >= 1:
            if not word[0] in node:
                node[word[0]] = Node(word[0])
            if len(word) == 1:
                node[word[0]].frequency = frequency
                node[word[0]].stop = True
            else:
                self._add_word(node[word[0]], word[1:], frequency)


    def add_word(self, word, frequency=1):
        """
        Adds a word to self.
        """
        word = word.lower()
        self._add_word(self.root, word, frequency)


    # @treevizer.recursion_viz
    def _remove(self, node, word):
        """
        Recursive method for removing a word
        """
        if word[0] not in node or (len(word) == 1 and not node[word[0]].stop):
            raise SearchMiss

        if len(word) > 1 and node[word[0]].children:
            self._remove(node[word[0]], word[1:])

        # Sets stop indicator to False

        if len(word) == 1 and node[word[0]].stop:
            node[word[0]].frequency = None
            node[word[0]].stop = False

        # Remove child if it's a leaf and not a word

        if not node[word[0]].children and not node[word[0]].stop:
            del node[word[0]]

    def remove(self, word):
        """
        Removes a word from self.
        """
        if word:
            word = word.lower()
            self._remove(self.root, word)
        else:
            raise SearchMiss

        return word

    def _find(self, node, word):
        """
        Recursive method. Searches for word in self,
        returns True if word is in self,
        otherwise returns False
        """
        if word and word[0] in node:
            if len(word) == 1:
                if node[word[0]].stop:
                    return True
                return False
            return self._find(node[word[0]], word[1:])
        return False

    def find(self, word):
        """
        Returns True if the word is in self,
        otherwise raises SearchMiss
        """
        word = word.lower()
        if not self._find(self.root, word):
            raise SearchMiss
        return True

    def __contains__(self, word):
        """
        Returns True if the word is in self,
        otherwise returns False.
        """
        word = word.lower()
        return self._find(self.root, word)

    def _word_count(self, node):
        """
        Recursive method for counting words in self
        """
        if node.stop:
            counter = 1
        else:
            counter = 0
        if node.children:
            for child in node.children.values():
                counter += self._word_count(child)
        return counter

    def word_count(self):
        """
        Returns number of word that self contains
        """
        return self._word_count(self.root)

    def __len__(self):
        """
        Returns the number of words self contains.
        """
        return self._word_count(self.root)

    def _all_words(self, node):
        """
        Recursive method for returnng all words in self
        """
        word_list = []
        if node.children:
            for child in node.children.values():
                word_list += self._all_words(child)
            if node.value and word_list:
                for index, word in enumerate(word_list):
                    word_list[index] = node.value + word
        if node.stop:
            word_list.append(node.value)
        return word_list

    def all_words(self):
        """
        Returns a list with all the words self contains,
        sorted in alphabetic order.
        """
        return sorted(self._all_words(self.root))

    def _sort_and_limit_ten(self, word_list):
        """
        Sorts list with words, highest frquency first and returns
        up to 10 words with highest frequency
        """
        if word_list:
            word_list.sort()
            word_list.sort(reverse=True, key=sort_on_freq)
            if len(word_list) > 10:
                word_list = word_list[0:10]

        return word_list

    def _return_endings(self, node):
        """
        Recursive helper method for the _prefix_search method.
        Returns up to 10 words based on highest frequency.
        (Method is called after we have passed the node that represents
        the last valueacter in the prefix)
        """
        word_list = []
        if node.children:
            for child in node.children.values():
                word_list += self._return_endings(child)
            if node.value and word_list:
                for index, word_freq in enumerate(word_list):
                    word, frequency = word_freq
                    word_list[index] = (node.value + word, frequency)
        if node.stop:
            word_list.append((node.value, node.frequency))

        if len(word_list) > 10:
            word_list = self._sort_and_limit_ten(word_list)

        return word_list

    def _prefix_search(self, node, prefix):
        """
        Recursive method for returning up to 10
        words that start with prefix
        """
        word_list = []

        # after this point all words start with the prefix,
        # so all words from the rest of the branch are included

        if len(prefix) == 1 and prefix in node:
            word_list += self._return_endings(node[prefix])

        # until we have passed "prefix" there is only one "path"

        elif len(prefix) > 1 and prefix[0] in node:
            word_list += self._prefix_search(node[prefix[0]], prefix[1:])
            if word_list:
                for index, word_freq in enumerate(word_list):
                    word, frequency = word_freq
                    word_list[index] = (prefix[0] + word, frequency)

        if len(word_list) > 10:
            word_list = self._sort_and_limit_ten(word_list)

        return word_list

    def prefix_search(self, prefix):
        """
        Returns up to 10 words with the highest
        frequency that start with the prefix.
        Returns a list with tuples with string on index 0 and
        frequency on index 1, sorted on frequency, highest first.
        If no words are found returns empty list.
        """
        word_list = []
        if prefix:
            prefix = prefix.lower()
            word_list = self._prefix_search(self.root, prefix)
            if len(word_list) <= 10:
                word_list = self._sort_and_limit_ten(word_list)
        return word_list

    def _correct_spelling(self, node, word):
        """
        Recursive method for finding misspelled words.
        Use for nodes that are not root
        """
        word_list = []

        if len(word) == 1 and node.value == word[0] and node.stop:
            return [node.value]

        if len(word) > 1 and node.children:
            for child_value in node.children:
                if node.value == word[0] or child_value == word[1]:
                    word_list += self._correct_spelling(node[child_value], word[1:])
        if word_list:
            for index, word_ in enumerate(word_list):
                word_list[index] = node.value + word_

        return word_list

    def correct_spelling(self, word):
        """
        If the word is spelled correctly, returns a list that contains
        only the word. Otherwise returns all words of same length as the word,
        where last at least each other letter is correct and where the last letter is correct.
        If no words are found an empty list is returned.
        """
        word_list = []
        if word:
            word = word.lower()
            if word in self:
                return [word]
            for child in self.root.children.values():
                child_list = self._correct_spelling(child, word)
                word_list += child_list
        return sorted(word_list)

    def _suffix_search(self, node, suffix):
        """
        Recursive method for finding all words that
        wnd with the suffix
        """
        word_list = []
        new_word_list = []


        # loop out to all leafs
        for child in node.children.values():
            word_list += self._suffix_search(child, suffix)

        # if current node not is root and the list
        # with returns from children is not empty
        if node.value and word_list:
            for word in word_list:
                # if the word is not yet confimed to end with suffix
                # check if current node's value corresponds to last letter
                # in the "remains" of suffix
                if word[1] and node.value == word[1][-1]:
                    # If yes, add current node's value to beginning of the word
                    # and append it together with ccorresponding slice of prefix
                    # minus last letter to the new word list
                    new_word_list.append((node.value + word[0], word[1][:-1]))
                elif not word[1]:
                    # If nothing is left of the prefix then just add current node's
                    # value to the word and append it to the new list
                    new_word_list.append((node.value + word[0], word[1]))

        # not node.value means it's the root node
        elif not node.value:
            # then we just pick out the words from the list with
            # words we got back from the children
            word_list = [i[0] for i in word_list]
            return word_list

        # if current node is a word and last letter
        # corresponds to last letter in suffix
        # add node's value as new word and suffix minus
        # one letter from the right
        if node.stop and node.value == suffix[-1]:
            new_word_list.append((node.value, suffix[:-1]))

        return new_word_list


    def suffix_search(self, suffix):
        """
        Returns a list containing all the words that end
        with the suffix. If no words are found an empty list is returned.
        """
        suffix = suffix.lower()
        word_list = self._suffix_search(self.root, suffix)
        return sorted(word_list)

    @classmethod
    def create_from_file(cls, filename="src/frequency.txt"):
        """
        Returns an instance of trie with information loaded from
        a txt file.
        """
        new_trie = cls()

        with open(filename, "r", encoding="utf-8") as fhand:
            content = fhand.readlines()

        for line in content:
            word, frequency = line.split()
            new_trie.add_word(word, float(frequency))

        return new_trie
