import unittest

import rdflib

from ontolawgy.tagger import tools


__author__ = 'fccoelho'


class Tests(unittest.TestCase):

    def test_load_ontology(self):
        o = tools.load_ontology()
        self.assertIsInstance(o, rdflib.Graph)

    def test_loaded_ontology_is_not_empty(self):
        o = tools.load_ontology()
        self.assertGreater(len(o.all_nodes()), 0)