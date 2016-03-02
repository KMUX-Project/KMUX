import unittest

from lib.graph import Graph


class TestGraph(unittest.TestCase):

    def testGrap(self):
        g = Graph()
        # g.addNode("test")
        g.addNode("b")
        g.addEdge("test1", "b")
        g.addEdge("test2", "b")
        g.addEdge("root", "test2")
        g.addEdge("c", "test2")
        #g.addEdge("b", "c")
        print(g.toDot())
        print(g.dfs())
