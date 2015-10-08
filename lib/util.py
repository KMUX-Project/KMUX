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
import json
import os
import jinja2
import importlib


class Utils:

    @staticmethod
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

    @staticmethod
    def loadModules():
        '''
        Search and load avaible modules dynamcially
        :return: dictionary { modulename : instance of loaded module }
        '''
        modules = Utils.searchModules()

        for modname in modules:
            modpath = "modules." + modname + ".scripts.main"
            module = importlib.import_module(modpath)
            my_class = getattr(module, "Main")
            inst = my_class(config)

    @staticmethod
    def genConfigIni():
        '''
        Generate the config-ini.json file that contains the initial kmux setup
        :return: the config ini file as dictionary
        '''
        modules = Utils.searchModules()
        temploader = jinja2.FileSystemLoader(
            searchpath=os.environ['PYTHONPATH'])
        env = jinja2.Environment(loader=temploader)
        template = env.get_template('./main/config-ini.json')
        config = json.loads(template.render())
        config['container'] = {}
        for modname in modules:
            modpath = "modules." + modname + ".scripts.main"
            module = importlib.import_module(modpath)
            my_class = getattr(module, "Main")
            instance = my_class({})
            modenabled = "off"
            if instance.isDefault:
                modenabled = "on"
            config['container'].update(
                {instance.getContainerName(): modenabled})
        if not os.path.exists('./config.out'):
            os.mkdir("./config.out")
        fout = open("./config.out/kmux-config-ini.json", "w+")
        json.dump(config, fout, indent=1)
