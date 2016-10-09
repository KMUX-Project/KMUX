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
import json
import glob


class Root():
    number = 10

    def __init__(self, name):
        self.dir = 'modules/' + name
        self.inifile = self.dir + '/config/ini.json'
        self.depfile = self.dir + '/config/dep.json'
        self.genfile = self.dir + '/templates/gen.kmux'
        self.instfile = self.dir + '/templates/inst.kmux'
        self.number = Root.number
        Root.number = Root.number + 1
        self.depfile = self.depfile
        self.basicconf = {}
        self.basicconf['nr'] = self.number
        self.basicconf['name'] = name
        self.inidict = {}

    def __renderConfig(self, tfile, vars):
        temploader = jinja2.FileSystemLoader(".")
        env = jinja2.Environment(loader=temploader)
        template = env.get_template(tfile)
        return json.loads(template.render(vars))

    def __renderTemplates(self, tfiles, vars, outpath):
        if tfiles == None or len(tfiles) == 0:
            return
        if not os.path.isdir(outpath):
            print("Could not find " + outpath)
            return
        temploader = jinja2.FileSystemLoader(".")
        env = jinja2.Environment(loader=temploader)
        for tfile in tfiles:
            template = env.get_template(tfile)
            out = template.render(vars)
            outdir = os.path.abspath(outpath + "/" + os.path.dirname(tfile))
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            outfile = outdir + "/" + \
                os.path.splitext(os.path.basename(tfile))[0]
            print("write to " + outfile)
            ofile = open(outfile, "w")
            ofile.write(out)
            ofile.close()

    def __findTemplates(self):
        return list(glob.iglob(self.dir + '/templates/**/*.tmpl'))

    def getNumber(self):
        return self.number

    def getDir(self):
        return self.dir

    def genIni(self, globconf):
        # take the parameters from the global configuration file
        self.basicconf.update(globconf)
        return self.__renderConfig(self.inifile, self.basicconf)

    def getIniFile(self):
        return self.inidict

    def genTemplates(self, globconf, outpath):
        tfiles = self.__findTemplates()
        self.__renderTemplates(tfiles, globconf, outpath)

    def getDependencies(self):
        return Json.readJSONFile(self.depfile)

    def getDepFile(self):
        return self.depfile
