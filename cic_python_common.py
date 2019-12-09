#!/usr/bin/python
"""A utility functions for Python that I found necessary to write."""

# Copyright (C) 2015-2019, Andrew Kroshko, all rights reserved.
#
# Author: Andrew Kroshko
# Maintainer: Andrew Kroshko <akroshko.public+devel@gmail.com>
# Created: Sat Mar 28, 2015
# Version: 20191209
# URL: https://github.com/akroshko/cic-python-common
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
from functools import wraps
import base64
import re
import struct
import types
import time
import getpass
import inspect
import string
import subprocess
import tempfile
import socket
import random
try:
    import psutil
except ImportError:
    pass

HOMEDIRECTORY=os.path.expanduser('~')

from cic_python_constants import BWhite,White,BRed,Red,BYellow,Yellow,BGreen,Green,On_Blue,On_Purple,On_Cyan,Color_Off

# TODO: improve how colors work in interactive functions
def yell(string):
    """Give a colored error message (red for now) along with the script
name that produced it.
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if hasattr(module,'__file__') and module.__file__:
        sys.stderr.write("%s%s: %s%s%s\n" % (BRed,os.path.basename(module.__file__),Red,string,Color_Off))
    else:
        sys.stderr.write("%s%s: %s%s%s\n" % (BRed,'python',Red,string,Color_Off))

def warn(string):
    """Give a colored warning message (yellow for now) along with the
script name that produced it.

    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if hasattr(module,'__file__') and module.__file__:
        sys.stderr.write("%s%s: %s%s%s\n" % (BYellow,os.path.basename(module.__file__),Yellow,string,Color_Off))
    else:
        sys.stderr.write("%s%s: %s%s%s\n" % (BYellow,'python',Yellow,string,Color_Off))

def msg(string):
    """Give a colored warning message (green for now) along with the
script name that produced it.

    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if hasattr(module,'__file__') and module.__file__:
        sys.stderr.write("%s%s: %s%s%s\n" % (BGreen,os.path.basename(module.__file__),Green,string,Color_Off))
    else:
        sys.stderr.write("%s%s: %s%s%s\n" % (BGreen,'python',Green,string,Color_Off))

def h1(string=None):
    """Give a colored first-level heading with an optional string
embedded.

    **Parameters**
      string:
        A string giving to be embedded in the headng.

    """
    if string:
        newstring = "==== %s ================================================================================" % string
    else:
        newstring = "======================================================================================="
    newstring = newstring[0:80]
    sys.stderr.write("%s%s%s%s\n" % (BWhite,On_Blue,newstring,Color_Off))

def h2(string=None):
    """Give a colored second-level heading with an optional string
emdedded.

    **Parameters**
      string:
        A string giving to be embedded in the headng.

    """
    if string:
        newstring = "---- %s ------------------------------------------------------------" % string
    else:
        newstring = "--------------------------------------------------------------------"
    newstring = newstring[0:60]
    sys.stderr.write("%s%s%s%s\n" % (BWhite,On_Cyan,newstring,Color_Off))

def h3(string=None):
    """Give a colored third-level heading with an optional string
embedded.

    **Parameters**
      string:
        A string giving to be embedded in the headng.

    """
    if string:
        newstring = "---- %s" % string
    else:
        newstring = "----"
    sys.stderr.write("%s%s%s%s\n" % (White,On_Purple,newstring,Color_Off))

# TODO: this is duplicated elsewhere
def convert_to_char(number):
    if number <= 25:
        # return chr(number+ord('a'))
        return chr((number)+ord('A'))
    elif number <= 35:
        return str(number-26)
    # TODO: there is still no reason no to include these
    # elif number <= 51:
    #     return chr((number-26)+ord('A'))
    # elif number <= 61:
    #     return str(number-52)
    else:
        raise RuntimeError()

# TODO: this is duplicated elsewhere
def generate_uid11():
    """Create a unique ID from a dictionary of atoms.  Should be reproducible given
    the same values.

    **Returns**
      string:
        An 11 character url-safe unique ID.  Only upper case and
        numbers are used to make these unique IDs easy to grep.  There
        are approximately 2**57 possibilities with about 454 million
        values expected before a collision.

    WARNING: These is not suitable for secure or cryptographic or
    production use, only for limited personal use where collisions are
    easily fixed by manual intervention.

    """
    return (convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)) +
            convert_to_char(random.randint(0,35)))

######################################################
## General path and environment variable functionality

def expand_all(path):
    """
    Expand the user and all environment variables in a path.

    **Arguments**:
      path : string
        The path to expand.

    **Returns**:
      string:
        The expanded path.
    """
    return os.path.expandvars(os.path.expanduser(path))

def makepath(path):
    """
    Recursively make a path if it does not exist.

    **Arguments**:
      path : string
        The path to check and make.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def read_posix_regexp(path):
    """This reads a posix regexes from the lines of a file, using or to
    paste them into a big regexp.  This generally only escapes things
    that have been required for applications.

    """
    firstline=True
    regexp=''
    fh = open(path,'r')
    for line in fh:
        if firstline:
            regexp+=line.strip().replace('\\\\','\\')
            firstline=False
        else:
            regexp+=('|'+line.strip()).replace('\\\\','\\')
    return regexp

def check_none_strip(string):
    """Return an empty string if none, otherwise strip whitespace.

    **Parameters**
      string:
        The string in question or None.

    **Returns**
      string:
        Either string stripped of whitespace or any empty string is
        parameter was None.

    """
    if string == None:
        return ''
    else:
        return string.strip()
