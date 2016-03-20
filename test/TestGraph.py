import unittest

from util.graph import Graph


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

        list1 = ['physics', 'chemistry', 1997, 2000]
        print("list2[1:]: ", list1[1:])
