#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import argparse
from blessings import Terminal
from modules.root import Root
import os
from util.graph import Graph
import json
from util.json import Json
from enum import Enum


class Mode(Enum):
    GENINI = 1
    GENKMUX = 2


def loadModules():
    '''
    Search and load avaible modules dynamcially
    :return: dictionary { modulename : instance of loaded module }
    '''
    moddict = {}
    modules = searchModules()
    for modname in modules:
        if not modname == 'root':
            moddict[modname] = Root(modname)

    return moddict


def searchModules():
    '''
    Search modules that are available
    :return: list of modules
    '''
    modules = []
    for root, dirs, files in os.walk('./modules'):
        for dir in dirs:
            name = dir
            if not name.startswith('_') and not name == 'root':
                modules.append(name)
        break
    return modules


def getDepGraph(moddict):
    depGraph = Graph()
    # build dependency graph
    for mod in moddict:
        deps = set(moddict[mod].getDependencies()["dependencies"])
        assert len(deps) <= 0 or deps.issubset(moddict.keys())
        for dep in deps:
            depGraph.addEdge(dep, mod)
    return depGraph


def loopOverModules(globconf, mode, outdir=None):
    moddict = loadModules()
    moddep = getDepGraph(moddict).dfs()
    ord = list(moddict.keys())
    completed = set()
    while len(ord) > 0:
        for n in ord:
            assert moddep.__contains__(n)
            moddeps = set(moddep[n])
            moddeps.difference_update(completed)
            if len(moddeps) == 0:
                if mode == Mode.GENINI:
                    globconf.update(moddict[n].genIni(globconf))
                else:
                    moddict[n].genTemplates(globconf, outdir)
                ord.remove(n)
                completed.add(n)

t = Terminal()

#print(t.bold('KMUX Manager'))
parser = argparse.ArgumentParser(description='KMUX Installation Helper.')
parser.add_argument('--list', help='list all modules', action="store_true")
parser.add_argument('--showdeps', action='store_true',
                    help='show depency structure')
parser.add_argument(
    '--genkmux', nargs=2,
    type=str,
    help='generate kmux.config.json from kmux-config-ini.json')
parser.add_argument(
    '--genini',
    help='generate kmux.config.ini',
    action="store_true")
args = parser.parse_args()

if (args.list):
    modules = searchModules()
    print(t.green(str(modules)))
elif (args.showdeps):
    moddict = loadModules()
    graph = getDepGraph(moddict)
    print(t.blue(graph.toDot()))
elif (args.genini):
    globconf = {}
    outdict = {}
    loopOverModules(globconf, Mode.GENINI)
    outdict['config'] = globconf
    print(json.dumps(outdict, indent=True))
elif (args.genkmux):
    config = Json.readJSONFile(args.genkmux[0])
    loopOverModules(config, Mode.GENKMUX, args.genkmux[1])
