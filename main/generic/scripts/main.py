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

from lib import Module
import sys
import jinja2
import os

sys.path.insert(0, '../../../lib')


class Generic(Module):

    def __init__(self, name, dist, ops, default, globconf):
        self.dir = 'main/modules/' + name
        self.conffile = self.dir + '/config.json'
        self.install = self.dir + '/create-generic.sh'
        self.basepackages = 'syslog-ng ssmtp cron-apt ' \
                            'libnss-ldap libpam-ldap ldap-utils'
        self.depend = []

        Module.__init__(
            self, name, dist, ops, default, self.basepackages, self.depend, globconf, self.conffile)

        self.templatevars.update(globconf)
        self.temploader = jinja2.FileSystemLoader(
            searchpath=os.environ['PYTHONPATH'])
        self.env = jinja2.Environment(loader=self.temploader)

    def renderConfig(self):
        self.setTemplateVars()
        template = self.env.get_template(self.conffile)
        out = template.render(self.templatevars)
        return out

    def renderInstall(self):
        template = self.env.get_template(self.install)
        out = template.render(self.templatevars)
        return out
