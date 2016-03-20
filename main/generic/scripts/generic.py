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

import sys
from util.util import Util
import os
import jinja2

sys.path.insert(0, '../../../lib')


class Generic():

    number = 0

    def __init__(self, name):

        self.dir = 'main/modules/' + name
        self.conffile = self.dir + '/config.json'
        self.inifile = self.dir + '/ini.json'
        self.depfile = self.dir + '/dep.json'
        self.number = ++Generic.number
        self.dependencies = Util.readJSONFile(self.depfile)
        self.basicconf = {}
        self.basicconf['nr'] = self.number
        self.basicconf['name'] = name
        self.inidict = {}

    def getNumber(self):
        return self.number

    def getDir(self):
        return self.dir

    def genIni(self, globconf):

        # take the parameters from the global configuration file
        self.basicconf.update(globconf)

        self.temploader = jinja2.FileSystemLoader(
            searchpath=os.environ['PYTHONPATH'])
        self.env = jinja2.Environment(loader=self.temploader)

        template = self.env.get_template(self.inifile)
        self.inidict = template.render(self.basicconf)

    def getIni(self):
        return self.inidict

    def getDependencies(self):
        return self.dependencies
