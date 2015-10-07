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

import argparse

from blessings import Terminal
from lib.util import Utils


t = Terminal()

print(t.bold('KMUX Manager'))
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--list', help='list all modules', action="store_true")
parser.add_argument(
    '--genconfig', help='generate kmux.config', action="store_true")
parser.add_argument(
    '--genini', help='generate kmux.config.ini', action="store_true")

args = parser.parse_args()

if (args.list):
    modules = Utils.searchModules()
    print(t.green(modules))
elif (args.genini):
    modules = Utils.genConfigIni()
    print(t.green("kmux-config-ini.json written to config.out/"))
