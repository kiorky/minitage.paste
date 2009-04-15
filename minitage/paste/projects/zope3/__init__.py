#!/usr/bin/env python

# Copyright (C) 2008, Mathieu PASQUET <kiorky@cryptelium.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__docformat__ = 'restructuredtext en'

import os
import sys
import getpass
import pwd
import grp
import subprocess

from minitage.paste.projects import common
from minitage.paste.common import var
from minitage.core.common import which


running_user = getpass.getuser()
gid = pwd.getpwnam(running_user)[3]
group = grp.getgrgid(gid)[0]

class Template(common.Template):
    """A Zope3 template"""

    summary = 'Template for creating a basic zope3 project'
    python = 'python-2.5'

    def post(self, command, output_dir, vars):
        common.Template.post(self, command, output_dir, vars)
        p = os.path.join(vars['path'], 'etc', 'zeoserver.sh.in')
        if os.path.exists(p):
            os.chmod(p, 0755)

    def pre(self, command, output_dir, vars):
        """register catogory, and roll in common,"""
        vars['category'] = 'zope'
        common.Template.pre(self, command, output_dir, vars)
        vars['mode'] = vars['mode'].lower().strip()
        if not vars['mode'] in ['zodb', 'relstorage', 'zeo']:
            raise Exception('Invalid mode (not in zeo, zodb, relstorage')

Template.vars = common.Template.vars \
        + [var('address',
               'Address to listen on',
               default = 'localhost',),
           var('port',
               'Port to listen to',
               default = '8080',),
           var('loglevel',
               'log level (DEBUG|INFO|WARNING|ERROR)',
               default = 'INFO',),
           var('debug',
               'Debug mode (on|off)',
               default = 'on',),
           var('zeoaddress',
               'Address for the zeoserver (zeo mode only)',
               default = 'localhost:8100',),
           var('mzeoaddress',
               'Address for the zeoserver monitor (zeo mode only)',
               default = 'localhost:8101',),
           var('user',
               'User',
               default = running_user,),
           var('passwd',
               'Password',
               default = 'admin',),
           var('version',
               'Version',
               default = '0.0.1',),
           var('author',
               'Author',
               default = running_user,),
           var('email',
               'Email',
               default = '%s@%s' % (running_user, 'localhost')),
           var('mode',
               'Mode to use: zodb|relstorage|zeo',
               default = 'zodb'),
           var('relstorage',
               'RelStorage support (yes|no)',
               default = 'yes'),
           var('plone_eggs',
               'space separeted list of additionnal eggs to install',
               default = '',),
           var('dbtype',
               'Relstorage database type (only useful for relstorage mode)',
               default = 'postgresql',),
           var('dbhost',
               'Relstorage database host (only useful for relstorage mode)',
               default = 'localhost',),
           var('dbport',
               'Relstorage databse port (only useful for relstorage mode)',
               default = '5432',),
           var('dbname',
               'Relstorage databse name (only useful for relstorage mode)',
               default = 'minitagedb',),
           var('dbuser',
               'Relstorage user (only useful for relstorage mode)',
               default = running_user),
           var('dbpassword',
               'Relstorage password (only useful for relstorage mode)',
               default = 'admin',),
           var('psycopg2',
               'Postgresql python bindings support (yes or no)',
               default = 'no',),
            var('mysqldb',
                'Python Mysql bindings support (yes or no)',
                default = 'no',),
]
# vim:set et sts=4 ts=4 tw=80:
