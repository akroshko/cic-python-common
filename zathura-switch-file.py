#!/usr/bin/env python
""" This file is used by zathura to go through files in a directory by alphabetic order or modification time. """
# Copyright (C) 2017-2018, Andrew Kroshko, all rights reserved.
#
# Author: Andrew Kroshko
# Maintainer: Andrew Kroshko <akroshko.public+devel@gmail.com>
# Created: Thu Jan 19 2017
# Version: 20180703
# URL: https://github.com/akroshko/python-stdlib-personal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

import os,sys
import re
import dbus

# TODO: make this a system wide importable constant
zathura_extension_patterns=['.*\.djvu$','.*\.pdf$']

# TODO: get rid of the test stuff
def main(argv):
    fh = open(os.path.expanduser('~/zathuratest.txt'),'w')
    # enumerate zathura instances
    bus = dbus.SessionBus()
    zathura_names = [n for n in bus.list_names() if 'zathura' in n]
    fh.write(str(zathura_names))
    fh.write('\n')
    proper_dbusname = None
    for dbusname in zathura_names:
        zathura_bus = bus.get_object(dbusname,'/org/pwmt/zathura')
        zathura_properties = dbus.Interface(zathura_bus,'org.freedesktop.DBus.Properties')
        properties = zathura_properties.GetAll('org.pwmt.zathura')
        fh.write(properties['filename'])
        fh.write('\n')
        fh.write(str(argv))
        fh.write('\n')
        if properties['filename'] == argv[1]:
            proper_dbusname = dbusname
    zathura_bus = bus.get_object(proper_dbusname,'/org/pwmt/zathura')
    # now get the directory of the one
    thedirname = os.path.dirname(argv[1])
    thefilename = os.path.basename(argv[1])
    # get list of files
    # decide whether we are ordering them by name or time based on argv 2
    if '--bytime' in argv:
        listoffiles = getfiles_by_mtime(thedirname,zathura_extension_patterns)
    else:
        listoffiles = getfiles_by_name(thedirname,zathura_extension_patterns)
    fh.write(str(listoffiles))
    fh.write('\n')
    # get position of current file in list
    current_position = listoffiles.index(thefilename)
    fh.write(str(current_position))
    fh.write('\n')
    # get next/previous file in list
    if '--bytime' in argv:
        # next generally means older
        if '--previous' in argv:
            newindex = current_position + 1
        else:
            newindex = current_position - 1
    else:
        if '--previous' in argv:
            newindex = current_position - 1
        else:
            newindex = current_position + 1
    newindex = newindex % len(listoffiles)
    newfile = listoffiles[newindex]
    # open the new file
    fh.write('Trying to open!!!')
    fh.write('\n')
    fh.flush()
    openmeth = zathura_bus.get_dbus_method('OpenDocument','org.pwmt.zathura')
    openmeth(os.path.join(thedirname,newfile),'',0)
    fh.write('Finished successfully')
    fh.write('\n')
    fh.close()

# TODO: the following functions are terrible python code

# https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
def getfiles_by_mtime(dirpath,patterns):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    aa = []
    for f in a:
        matched=False
        for p in patterns:
            if re.match(p,f,re.IGNORECASE):
                matched=True
                if matched:
                    aa.append(f)
    aa.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return aa

def getfiles_by_name(dirpath,patterns):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    aa = []
    for f in a:
        matched=False
        for p in patterns:
            if re.match(p,f,re.IGNORECASE):
                matched=True
                if matched:
                    aa.append(f)
    aa.sort(key=lambda s: s)
    return aa

if __name__ == '__main__':
    main(sys.argv)
