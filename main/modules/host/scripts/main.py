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

from main.generic.scripts.main import Generic
import sys
import os

sys.path.insert(0, '../../..')


class Main(Generic):

    def __init__(self, jsonglob):
        modpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        modname = os.path.basename(modpath)
        Generic.__init__(self, modname, 'sarge', 'debian',  jsonglob)
