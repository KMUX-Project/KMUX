#!/usr/bin/python3
'''
KMUX - a free and open source small business server.
Copyright (C) 2015, Julian Thomé <julian.thome.de@gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from collections import defaultdict

import sys


class Edge:

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def __str__(self):
        return self.src + "->" + self.dest


class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.outgoing = defaultdict(list)
        self.incoming = defaultdict(list)
        self.time = 0
        self.d = defaultdict(list)
        self.f = defaultdict(list)
        self.color = defaultdict(list)
        self.parent = defaultdict(list)
        self.pred = defaultdict(list)

    def addEdge(self, src, dest):
        e = Edge(src, dest)
        self.nodes.add(src)
        self.nodes.add(dest)
        self.edges.add(e)

        if self.incoming.get(dest) == None:
            self.incoming[dest] = []

        if self.outgoing.get(src) == None:
            self.outgoing[src] = []

        self.incoming[dest].append(src)
        self.outgoing[src].append(dest)

    def addNode(self, nod):
        self.nodes.add(nod)

    def __str__(self):
        str = ""
        for e in self.edges:
            str = str + "\n" + e.__str__()

        return str

    def toDot(self):
        str = "digraph G {\n"
        for e in self.edges:
            str += "\t" + e.__str__() + ";\n"

        str += "}"

        return str

    def dfs(self):

        for s in self.nodes:
            self.color[s] = "white"
            self.pred[s] = []

        for s in self.nodes:
            if self.color[s] == "white":
                self.dfsVisit(s)
            elif self.color[s] == "gray":
                print("Error: there is a cyclic dependency between modules")
                sys.exit(-1)

        return self.pred

    def dfsVisit(self, s):

        self.time = self.time + 1
        self.d[s] = self.time
        self.color[s] = "gray"

        succlist = self.outgoing.get(s)

        if succlist != None:
            #print(" S " + s + " succlist " + str(succlist))
            for succ in succlist:
                #print("COL " + str(self.color))
                if self.color[succ] == "gray":
                    sys.exit(-1)
                elif self.color[succ] == "white":
                    self.dfsVisit(succ)

                self.pred.get(succ).append(s)
        self.color[s] = "black"
        self.time = self.time + 1
        self.f[s] = self.time
