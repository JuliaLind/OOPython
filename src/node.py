#!/usr/bin/env python3
"""
Node class
"""

class Node:
    """
    Class that represents a node
    """
    def __init__(self, value=None, frequency=None):
        """
        Constructor
        """
        self.children = {}
        self.value = value
        self.frequency = frequency
        self.stop = False

    def __setitem__(self, key, node):
        """
        Adds a childnode that represents the key
        """
        self.children[key] = node

    def __getitem__(self, key):
        """
        Returns the childnode that represents the key
        """
        return self.children[key]

    def __delitem__(self, key):
        """
        Deletes a childnode that represents the key
        """
        del self.children[key]

    def __contains__(self, key):
        """
        Returns True if self has a childnode that represents
        the key, otherwise returns False
        """
        return key in self.children
