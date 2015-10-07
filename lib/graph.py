#!/usr/bin/python3
'''
KMUX - a free and open source small business server.
Copyright (C) 2015, KMUX Project

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

    def addEdge(self, src, dest):
        e = Edge(src, dest)
        self.edges.add(e)

    def addNode(self, nod):
        self.nodes.add(nod)

    def __str__(self):
        str = ""
        for e in self.edges:
            str = str + "\n" + e.__str__()

        return str
