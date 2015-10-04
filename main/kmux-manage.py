#!/usr/bin/python3
'''
KMUX - an open source small business server.
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

import argparse
import os
import importlib
import json
import jinja2

from blessings import Terminal


confdict = {}

t = Terminal()

print(t.bold('KMUX Manager'))
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--list', help='list all modules', action="store_true")
parser.add_argument(
    '--genconfig', help='generate kmux.config', action="store_true")

args = parser.parse_args()

if (args.list):
    print("Searching for modules ...")
    print("... done")
elif (args.genconfig):
    print("Generate kmux.config ...")
    print("... done")

modules = []

for root, dirs, files in os.walk('./modules'):
    for dir in dirs:
        name = dir
        if not name.startswith('_'):
            print(t.green('Found Module ' + name))
            modules.append(name)
    break

temploader = jinja2.FileSystemLoader(
    searchpath=os.path.dirname(os.path.realpath(__file__)))
env = jinja2.Environment(loader=temploader)
template = env.get_template('./config.json')
config = json.loads(template.render())
config['container'] = {}

for modname in modules:
    modpath = "modules." + modname + ".scripts.main"
    module = importlib.import_module(modpath)
    my_class = getattr(module, "Main")
    inst = my_class(config)
    fout = open("./config.out/" + inst.getContainerName() + "-install.sh", "w")
    str = inst.renderInstall()
    fout.write(str)
    fout.close()

    modconf = inst.renderConfig()
    modconfdict = json.loads(modconf)
    config['container'].update(modconfdict)

fout = open("./config.out/kmux.config", "w")
json.dump(config, fout, indent=1)

print(t.bold('Have a look at config.out'))
