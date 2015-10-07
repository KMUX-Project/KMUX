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


class Module:

    number = 0

    def __init__(self, name, dist,
                 ops, default, packages, depend,
                 globconf, confpath):
        self.name = name
        self.dist = dist
        self.ops = ops
        self.default = default
        self.confpath = confpath
        self.basepackages = packages
        self.depend = depend

        self.globconf = globconf
        self.setTemplateVars()
        Module.number += 1

    def __str__(self):
        return self.name

    def create(self):
        print('create ' + ' ' + self.name + ' ' + self.dist)

    def getNumber(self):
        return Module.number

    def isDefault(self):
        return self.default

    def getContainerName(self):
        return self.name

    def getDependencies(self):
        return self.depend

    def setTemplateVars(self):
        self.templatevars = {"name": self.name,
                             "nr": Module.number,
                             "dist": self.dist,
                             "os": self.ops,
                             "basepackages": self.basepackages,
                             "depend": self.depend}
        self.templatevars.update(self.globconf)
