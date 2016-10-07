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
from main.skel import Skel
import os
from util.graph import Graph
import json


def loadModules():
    '''
    Search and load avaible modules dynamcially
    :return: dictionary { modulename : instance of loaded module }
    '''

    moddict = {}

    modules = searchModules()

    for modname in modules:
        print("load " + modname)
        moddict[modname] = Skel(modname)

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
            if not name.startswith('_'):
                modules.append(name)
        break
    return modules


t = Terminal()

print(t.bold('KMUX Manager'))
parser = argparse.ArgumentParser(description='KMUX Installation Helper.')
parser.add_argument('--list', help='list all modules', action="store_true")
parser.add_argument(
    '--genconfig', nargs=1,
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
elif (args.genini):
    #modules = Utils.genConfigIni()

    depGraph = Graph()
    moddict = loadModules()

    # build dependency graph
    for mod in moddict:
        deps = set(moddict[mod].getDependencies()["dependencies"])
        assert len(deps) <= 0 or deps.issubset(moddict.keys())
        for dep in deps:
            depGraph.addEdge(dep, mod)
    # check for cycles -- ensure graph is a DAG
    moddep = depGraph.dfs()

    ord = list(moddict.keys())

    globconf = {}
    completed = set()

    while len(ord) > 0:
        for n in ord:
            assert moddep.__contains__(n)
            moddeps = set(moddep[n])
            moddeps.difference_update(completed)
            if len(moddeps) == 0:
                moddict[n].genIni(globconf)
                ord.remove(n)
                completed.add(n)
                globconf.update(json.loads(moddict[n].getIni()))
                # globconf.update(moddict[mod].getIni())

    print(json.dumps(globconf, indent=True))

    print(t.green("kmux-config-ini.json written to config.out/"))
elif (args.genconfig):
    config = Utils.readJSONFile(args.genconfig[0])
    moddict = loadModules(config)
    print(t.green("kmux-config.json written to config.out/"))
