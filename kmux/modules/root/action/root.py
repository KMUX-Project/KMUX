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
from util.json import Json
import os
import jinja2


class Root():

    number = 10

    def __init__(self, name):

        self.dir = 'modules/' + name
        self.inifile = self.dir + '/config/ini.json'
        self.depfile = self.dir + '/config/dep.json'
        self.tempinst = self.dir + '/templates/gen.kmux'
        self.tempgen = self.dir + '/templates/inst.kmux'
        self.number = Root.number
        Root.number = Root.number + 1
        self.depfile = self.depfile
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
        self.temploader = jinja2.FileSystemLoader(".")
        self.env = jinja2.Environment(loader=self.temploader)
        template = self.env.get_template(self.inifile)
        self.inidict = template.render(self.basicconf)

    def getIni(self):
        return self.inidict

    def getDependencies(self):
        return Json.readJSONFile(self.depfile)

    def getDepfile(self):
        return self.depfile
