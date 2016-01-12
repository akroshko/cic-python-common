#!/usr/bin/env python
"""A standard set of utility and system administration functions."""

# Copyright (C) 2015 Andrew Kroshko, all rights reserved.
#
# Author: Andrew Kroshko
# Maintainer: Andrew Kroshko <akroshko@gmail.com>
# Created: Sat Mar 28, 2015
# Version: 20150522
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

from functools import wraps
import base64
import os
import sys
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

# make a translation table for comparing paths together
# TODO: can I put these into constants?
BACKSLASH_TRANSLATE = string.maketrans('\\','/')
SLASH_TRANSLATE = string.maketrans('/','\\')
DASH_TRANSLATE = string.maketrans('-','_')
PATH_DELIMETER = os.pathsep

from python_stdlib_constants import BWhite,White,BRed,Red,BYellow,Yellow,BGreen,Green,On_Blue,On_Purple,Color_Off

def int64_base64(n):
    """
    Convert the lower 48bits of an integer into a url-safe base-64.
    http://www.fuyun.org/2009/10/how-to-convert-an-integer-to-base64-in-python/

    **Parameters**
      n : integer
          The integer to be converted, of which the 48 bits are most important.

    **Returns**
      string:
          n as a base-64 url-safe string, 8 characters long.

    """
    data = struct.pack('<Q',n & 0xFFFFFFFFFFFFFFFFL).rstrip('\x00')
    if len(data) == 0:
        data = '\x00'
    s = base64.urlsafe_b64encode(data).rstrip('=')
    return s


def generate_uid():
    """
    Create a unique ID from a dictionary of atoms.  Should be reproducible given
    the same values.

    **Returns**
      string:
           An 8 character url-safe unique ID, reflecting 2**48 possibilities.
           With 1e6 of these uids, there is a probability of 0.0017747 of a
           collision.

    """
    return int48_base64(random.randint(0,2**64-1))

def generate_uid11():
    """
    Create a unique ID from a dictionary of atoms.  Should be reproducible given
    the same values.

    **Returns**
      string:
           An 8 character url-safe unique ID, reflecting 2**48 possibilities.
           With 1e6 of these uids, there is a probability of 0.0017747 of a
           collision.

    """
    # TODO: Create by hashing the hash values of the elements.  Do we really want
    #       to do this, or stick with just random uid's?
    # TODO: Only uses random numbers right now, maybe this is best?
    # XXXX: this isn't a real UID function at all!!!  Can I improve this?
    # run the generator a bit for fun
    for i in xrange(random.randint(64,128)):
        n1 = random.randint(0,2**64-1)
        n2 = random.randint(0,2**64-1)
    n1 = random.randint(0,2**64-1)
    n2 = random.randint(0,2**64-1)
    data1 = struct.pack('<Q',n1 & 0xFFFFFFFFFFFFL).rstrip('\x00')
    data2 = struct.pack('<Q',n2 & 0xFFFFFFFFFFFFL).rstrip('\x00')
    if len(data1) == 0:
        data1 = '\x00'
    if len(data2) == 0:
        data2 = '\x00'
    return (base64.urlsafe_b64encode(data1).rstrip('=')+base64.urlsafe_b64encode(data2).rstrip('='))[0:11]

def int48_base64(n):
    """
    Convert the lower 48bits of an integer into a url-safe base-64.
    http://www.fuyun.org/2009/10/how-to-convert-an-integer-to-base64-in-python/

    **Parameters**
      n : integer
          The integer to be converted, of which the 48 bits are most important.

    **Returns**
      string:
          n as a base-64 url-safe string, 8 characters long.

    """
    data = struct.pack('<Q',n & 0xFFFFFFFFFFFFL).rstrip('\x00')
    if len(data) == 0:
        data = '\x00'
    s = base64.urlsafe_b64encode(data).rstrip('=')
    return s

#########################################
## Utility function for use in decorators

def is_list(lst):
    """
    Is this a type of list?

    **Parameters**:
      obj : object
        The object to check.

    **Returns**:
      boolean:
        Indicates whether the object is a list.
    """
    return type(lst) == types.ListType

def make_list(obj):
    """
    Check if the argument is a 'list', if not, make it one and return.

    **Arguments**:
        obj : {object, list}

    **Returns**:
      list:
        'obj' in a list, or the original list.
    """
    if is_list(obj):
        return obj
    else:
        return [obj]

def args_to_list(*args,**kwargs):
    """
    Process positional arguments into a list.

    **Parameters**:
      *args : tuple
         The positional arguments to process into a list.
      **kwargs : dict
         Must be empty.

    **Returns**:
      list:
        *args as a list
    """
    if len(kwargs) > 0:
        raise ValueError
    if len(args) == 0:
        new_args = []
    if len(args) == 1:
        new_args = make_list(args[0])
    if len(args) > 1:
        new_args = list(args)
    return new_args

def any_items_nonzero(dictionary):
    """
    Are any items in this dictionary non-zero?

    **Parameters**:
      dictionary : dict
        The dictionary to check.

    **Returns**:
      boolean:
        Indicates if any items are non-zero.
    """
    nonzero = False
    for key in dictionary:
        if dictionary[key] != 0:
            nonzero = True
    return nonzero

def strip_double_quote_string(string):
    """
    Strip whitespace from a string and double-quote it.

    **Parameters**:
      string : str

    **Returns**:
      The new string.

    """
    stripped = string.strip()
    if not stripped[0] == '"' and stripped[-1] == '"':
        return '"' + stripped + '"'
    else:
        return stripped

####################
# TODO: expand decorator documentation

class CheckFailed(Exception):
    """ Exception raised if a check fails. """
    pass

def check_fail_ignore(func):
    """Decorator to ignore argument check exceptions"""
    @wraps(func)
    def new_func(*args,**kwds):
        try:
            return func(*args,**kwds)
        except CheckFailed:
            return None

class CheckArguments(object):
    """Decorator to check a particular argument"""
    def __init__(self,*args,**kwds):
        self.args = args_to_list(*args,**kwds)

    def __call__(self,func):
        @wraps(func)
        def new_func(*args,**kwds):
            for a in self.args:
                if is_int(a):
                    if not self.check(args[a]):
                        # TODO raise exception here?
                        raise CheckFailed
                elif is_string(a) and checkdk(kwds,a):
                    if not self.check(kwds[a]):
                        # TODO raise exception here?
                        raise CheckFailed
            return func(*args,**kwds)
        return new_func

class ProcessArguments(object):
    """ Process the *args and **kwds arguments used in method calls """
    def __init__(self,*args,**kwargs):
        self.args = args_to_list(*args,**kwargs)

    def __call__(self,func):
        @wraps(func)
        def new_func(*args,**kwargs):
            # Extract methods... no need to 'if' each time...
            new_args = list(args)
            new_kwargs = kwargs.copy()
            for a in self.args:
                if is_int(a):
                    new_args[a] = self.process(args[a])
                elif is_string(a) and checkdk(kwargs,a):
                    new_kwargs[a] = self.process(kwargs[a])
            new_args = tuple(new_args)
            return func(*new_args,**kwargs)
        return new_func

################
## Regex helpers

def list_match(index,pattern):
    """
    Return a closure for matching elements of a list to a pattern.

    **Parameters**:
      index : int or string
        The index in the list to match or 'all' for all indices.
      pattern : string
        The regexp pattern.

    **Returns**:
      The closure, a function taking an lst argument.
    """
    def unseen(lst):
        if index == 'all':
            return any([pattern.match(e) for e in lst])
        else:
            return pattern.match(lst[index])
    return unseen

################
## Type checking

def checkdk(dictionary,key):
    """
    Check that a dictionary key exists.

    **Parameters**:
      dictionary : dictionary
        The dictionary within to check for the key.
      key : hashable
        The dictionary key to check for in ''dictionary''.

    **Returns**:
      boolean:
        Indicates if the dictionary key exists.
    """
    return dictionary.has_key(key)

def is_int(obj):
    """
    Is this a type of integer?

    **Parameters**:
      obj : object
        The object to check.

    **Returns**:
      boolean:
        Indicates whether the object is an integer.
    """
    return type(obj) == types.IntType

def is_list_tuples(lst):
    """
    Is this a list of tuples?

    **Parameters**:
      obj : object
        The object to check.

    **Returns**:
      boolean:
        Indicates whether the object is a list of tuples.
    """
    if not is_list(lst):
        return False
    # not all tuples
    not_all_tups = False
    for item in lst:
        if not is_tuple(item):
            not_all_tups = not is_tuple(item)
    return not not_all_tups

#############
## Decorators

class MakeList(ProcessArguments):
    """ Turn a particular argument into a list if it already isn't one. """
    def __init__(self,*args,**kwds):
        ProcessArguments.__init__(self,*args,**kwds)
        self.process = make_list

def is_nothing(argument):
    """
    Is this ''None'' or an empty string after stripping whitespace?

    **Parameters**:
      argument : object
        The object to check.

    **Returns**:
      boolean:
        Indicates if the object is ''None'' or an empty string.
    """
    if argument is None:
        return True
    if type(argument) == type('') and argument.strip() == '':
        return True
    return False

def is_string(obj):
    """
    Is this a string?

    **Parameters**:
      argument : object
        The object to check.

    **Returns**:
      boolean:
        Indicates if the object is a string.
    """
    return type(obj) == types.StringType

def is_tuple(obj):
    """
    Is this a tuple?

    **Parameters**:
      argument : object
        The object to check.

    **Returns**:
      boolean:
        Indicates if the object is a string.
    """
    return type(obj) == types.TupleType

def none_none(lst):
    """
    Are there any None objects in a list?

    **Parameters**:
      lst : list
        The list of objects to check.

    **Returns**:
      boolean:
        Indicates that there are no Nones in the list.
    """
    found_none = False
    for item in lst:
        if item is None:
            found_none = True
    return not found_none

def uniquify(seq):
    """
    Make a sequence of items unique.

    **Parameters**:
      seq : An iterable sequence.

    **Returns**:
      list:
        The new sequence with unique items.
    """
    unique = []
    [unique.append(i) for i in seq if not unique.count(i)]
    return unique

####################
## Output formatting

def list_columns(lst):
    """
    Turn a list of strings into a column seperated by newlines.

    **Parameters**:
      lst : list
        The list to turn into columns.

    **Returns**:
      string:
        The column with elements seperated by newlines.

    """
    full_string = ''
    for column in lst:
        full_string += column + '\n'
    return full_string.strip()

def lol_columns(lol):
    """
    Turn a list of lists of strings into a set of columns seperated by
    newlines.

    **Parameters**:
      lol : list of lists
        The list of lists to turn into columns.

    **Returns**:
      string:
        The string representing the set of columns seperated by newlines.

    """
    # find maximum column size for each column
    column_sizes = []
    for row in lol:
        for number,column in enumerate(row):
            column_length = len(column.strip())
            # add the next column if it doesn't already exist
            if len(column_sizes) < number + 1:
                column_sizes.append(0)
            column_sizes[number] = max(column_length,column_sizes[number])
    # format and output the columns
    full_string = ''
    for row in lol:
        row_string = ''
        for number,column in enumerate(row):
            row_string += column.strip().ljust(column_sizes[number]) + ' '
        full_string += row_string + '\n'
    return full_string.strip()

def lol_load(lines):
    """
    Load a string representing rows and columns into a list of lists.

    This function may be deprecated soon.

    **Parameters**:
      lines: string
        A string representing rows and columns, delineated by one-word
        headers and ended by new-lines, into a list of lists.

    **Returns**:
      list of lists:
        The list of lists from the parsed string.
    """
    # get the first row to get the column widths
    splits = re.split('(\s+)',lines[0])
    words = splits[::2]
    spaces = splits[1::2]
    # parse the rest of the columns
    columns = []
    spaces_max = len(spaces)-1
    for index,word in enumerate(words):
        if index < spaces_max:
            columns.append(words[index]+spaces[index])
        else:
            columns.append(words[index])
    columns = filter(lambda s: s != '',columns)
    column_lengths = [len(c)-1 for c in columns]
    boundaries = []
    boundaries.append((0,column_lengths[0]))
    for index,length in enumerate(column_lengths[:-1],1):
        if  index < len(column_lengths):
            boundaries.append((boundaries[index-1][1]+1,
                               boundaries[index-1][1]+1+column_lengths[index]))
    lol = []
    # XXXX: other code that uses this only works if this is [0:]
    for line in lines[0:]:
        lst = []
        for boundary in boundaries[:-1]:
            lst.append((line[boundary[0]:boundary[1]]).strip())
        lst.append((line[boundaries[-1][0]:]).strip())
        lol.append(lst)
    return lol

########################
## Configuration helpers
def get_command_output(command,cwd=None):
    """
    Get the output of a command.

    **Arguments**:
      command : string
        The command to get the output from.
    **Returns**:
      string:
        The output of the command.
    """
    # http://docs.python.org/library/subprocess.html?highlight=subprocess#subprocess.Popen
    # helpful hints on getting shell=False to work
    p = subprocess.Popen(command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         bufsize=0,
                         cwd=cwd)
    comm = p.communicate()
    stdout = comm[0].strip()
    return stdout

def get_user():
    """
    Get the current user.

    **Returns**:
      string:
        The current user.
    """
    return getpass.getuser()

def get_home():
    """
    Get the current home.

    **Returns**:
      string:
        The current home directory.
    """
    current_home = os.path.expanduser('~')
    return current_home

##################
## Command helpers

def command_call_string(command_call):
    """
    Call a command or Python function depending on what is passed.

    **Arguments**:
      command_call : command object
        A list of command arguments used by subprocess.Popen.
        A tuple of (python_function,[command args],kwds)

    **Returns**:
      string:
        Formatted output of the command.
    """
    if is_tuple(command_call):
        string = 'Python function: ' + command_call[0].__name__ + '\n'
        string += 'Command: ' + ' '.join(command_call[1]) + '\n'
        if len(command_call) == 3:
            string += 'kwds: ' + command_call[2] + '\n'
    else:
        string = 'Command: ' + ' '.join(command_call) + '\n'
    return string

def write_zero_newlines(string,stream=sys.stdout):
    """
    Write a string with zero trailing newlines to a stream.

    **Arguments**:
      string : string
        The string to write.
      stream: stream
        The stream to write defaulting to sys.stdout.
    """
    stream.write(string.strip())

def write_one_newline(string,stream=sys.stdout):
    """
    Write a string that always has one trailing newlines to a stream.

    **Arguments**:
      string : string
        The string to write.
      stream: stream
        The stream to write defaulting to sys.stdout.
    """
    # XXXX: not working terribly well for terminal stuff
    stream.write(string.strip() + '\n')

def write_two_newline(string,stream=sys.stdout):
    """
    Write a string that always has two trailing newlines to a stream.

    **Arguments**:
      string : string
        The string to write.
      stream: stream
        The stream to write defaulting to sys.stdout.
    """
    # XXXX: not working terribly well for terminal stuff
    stream.write(string.strip() + '\n\n')

def multi_command_output(*commands):
    """

    **Arguments**:
      *commands : command object
        A list of lists of command arguments used by subprocess.Popen.
        A list of tuples of (python_function,[command args],kwds)

    **Returns**:
      list of integers : The list of returncodes from the commands.
    """
    command_strings = []
    p_list = []
    for command in commands:
        # get the command string
        command_strings.append(command_call_string(command))
    # give the list of commands to run and number them
    for i,command in enumerate(command_strings):
        write_one_newline('[' + str(i+1) + '] ' + command)
        sys.stdout.flush()
    # extract the commands
    for command in commands:
        # run the command if it's a command tuple
        if is_tuple(command):
            if len(command) == 3:
                p_list.append(globals()[command[0].__name__](command[1],**command[2]))
            else:
                # TODO examine MakeList function
                p_list.append(globals()[command[0].__name__](command[1]))
        # run the command if it's just an argument list
        else:
            # create two temp files
            stdout_fh = os.fdopen(tempfile.mkstemp()[0],'r+')
            stderr_fh = os.fdopen(tempfile.mkstemp()[0],'r+')
            p = subprocess.Popen(command,
                                 stdout=stdout_fh,
                                 stderr=stderr_fh,
                                 stdin=subprocess.PIPE,
                                 bufsize=0,
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
            p.stdout_fh = stdout_fh
            p.stderr_fh = stderr_fh
            p_list.append(p)
    # wait for all commands to finish
    last_poll_list = [None] * len(command_strings)
    done = False
    while not done:
        poll_list = [p.poll() for p in p_list]
        # find differences and display them
        for i,poll in enumerate(poll_list):
            if last_poll_list[i] is None and poll_list[i] is not None:
                write_one_newline('[' + str(i+1) + '] done with return code ' + str(p_list[i].returncode))
                sys.stdout.flush()
        if none_none(poll_list):
            done = True
        last_poll_list = poll_list
        time.sleep(2)
    # collect stderr and stdout into variables and display along with command string
    # TODO pop open new terminals???
    output = ''
    returncodes = []
    for index,p in enumerate(p_list):
        output += '================================================================================\n'
        output += command_strings[index].strip() + '\n'
        # TODO check for just two \n\n at the end?
        stdout_fh = p.stdout_fh
        stderr_fh = p.stderr_fh
        stdout_fh.seek(0)
        stderr_fh.seek(0)
        output += 'Stdout:\n' + stdout_fh.read() + '\n\n'
        output += 'Stderr:\n' + stderr_fh.read() + '\n\n'
        stdout_fh.close()
        stderr_fh.close()
        returncodes.append(p.returncode)
        output += 'Return code: ' + str(p.returncode).strip() + '\n'
    output += '================================================================================\n'
    # output the output in a cross-platform way
    # don't need newlines as echo adds them
    # TODO try out printing, better way than echo command!
    print output
    return returncodes

def call_list_to_string(command):
    """
    Convert a list of arguments like used by Popen to a string.

    XXXX: Just uses a basic .join for now.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.
      hosts : list of hosts
        Used by decorator or as a dummy argument.
      **kwds :
        Keywords to pass to subprocess.Popen.

    **Returns**:
      string:
        The string derived from the call list.

    """
    if not is_list(command):
        return command
    else:
        return ' '.join(command)

@MakeList(0)
def check_hosts(hosts):
    """
    Indicate if current host is in list of hosts.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.
      hosts : list of hosts
        Used by decorator or as a dummy argument.
      **kwds :
        Keywords to pass to subprocess.Popen.

    **Returns**:
      boolean:
        Indicate if current host is in list of hosts.
    """
    # host checking is disabled!!!
    if hosts == [None]:
        return True
    hostname = socket.gethostname()
    return list(set(hosts) & set([hostname,
                                  socket.gethostbyname(hostname),
                                  socket.getfqdn()])) \
            != []

class CheckHosts(CheckArguments):
    "Decorator to only run a particular function for valid hosts."
    def __init__(self,*args,**kwds):
        CheckArguments.__init__(self,*args,**kwds)
        self.check = check_hosts

def check_process(process_name):
    """
    Check if the a process is running.

    **Arguments**:
      process_name : string
        The name of the process to check.

    **Returns**:
      Empty list if process not found, otherwise list of matching process
       names.

    """
    processes = psutil.get_process_list()
    process_names = [p.name for p in processes]
    return filter(lambda s: process_name in s, process_names)

@CheckHosts('hosts')
@MakeList(0)
def call_native(command,hosts=None,**kwds):
    """
    Call the command using the subprocess call.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.
      hosts : list of hosts
        Used by decorator or as a dummy argument.
      **kwds :
        Keywords to pass to subprocess.Popen.

    **Returns**:
      subprocess.Popen :
        The subprocess.Popen object from calling the command.
    """
    return subprocess.call(command,*kwds)

@CheckHosts('hosts')
@MakeList(0)
def call_native_capture(command,hosts=None,**kwds):
    """
    Call the command using the subprocess call and capture output.

    XXXX: name will likely change

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.
      hosts : list of hosts
        Used by decorator or as a dummy argument.
      **kwds :
        Keywords to pass to subprocess.Popen.

    **Returns**:
      subprocess.Popen :
        The subprocess.Popen object from calling the command.
    """
    return subprocess.Popen(command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            bufsize=0,
                            **kwds)

@CheckHosts('hosts')
@MakeList(0)
def call_native_background(command,hosts=None,**kwds):
    """
    Call using the standard subprocess call in the background and
    capture output.

    XXXX: name will likely change, only works for sh-type shells.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.

      hosts :
        Used by decorator or dummy argument.
      **kwds :
        Keywords to pass to Popen.

    **Returns**:
      subprocess.Popen :
        The subprocess.Popen object from calling the command.
    """
    return subprocess.call(command + ['&','>>','/dev/null'],**kwds)

@CheckHosts('hosts')
@MakeList(0)
def call_native_background_capture(command,hosts=None,**kwds):
    """
    Call using the standard subprocess call in the background and
    capture output.

    XXXX: name will likely change, only works for sh-type shells.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.
      hosts : list of hosts
        Used by decorator or as a dummy argument.
      **kwds :
        Keywords to pass to subprocess.Popen.

    **Returns**:
      subprocess.Popen :
        The subprocess.Popen object from calling the command.
    """
    # have a log for cic commands? In a var directory?
    return subprocess.Popen(command + ['&','>>','/dev/null'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            bufsize=0,
                            **kwds)


@CheckHosts('hosts')
@MakeList(0)
def call_bash_env(command,hosts=None,**kwds):
    """
    Call using the standard subprocess call along with a bash shell.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.

      hosts :
        Used by decorator or dummy argument.
      **kwds :
        Keywords to pass to Popen.

    **Returns**:
      subprocess.Popen :
        The subprocess.Popen object from calling the command.
    """
    # TODO shlex?
    # TODO other shells?
    #      merge lists?
    return subprocess.call(['bash','--init-file',os.path.expanduser('~/.bash_env'),'-c'] + [' '.join(command)],**kwds)

@CheckHosts('hosts')
@MakeList(0)
def call_bash(command,hosts=None,**kwds):
    """
    Call using the standard subprocess call along with a bash shell.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.

      hosts :
        Used by decorator or dummy argument.
      **kwds :
        Keywords to pass to Popen.

    **Returns**:
      subprocess.Popen :
        The subprocess.Popen object from calling the command.
    """
    # TODO shlex?
    # TODO other shells?
    #      merge lists?
    return subprocess.call(['bash','--login','-c'] + [' '.join(command)],**kwds)

@CheckHosts('hosts')
@MakeList(0)
def call_bash_capture(command,hosts=None,**kwds):
    """
    Call using the standard subprocess call along with a bash shell
    and capture output.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.
      hosts : list of hosts
        Used by decorator or as a dummy argument.
      **kwds :
        Keywords to pass to subprocess.Popen.

    **Returns**:
      subprocess.Popen :
        The subprocess.Popen object from calling the command.
    """
    # TODO other shells?
    #      merge lists?
    return subprocess.Popen(['bash','--login','-c'] + [' '.join(command)],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            bufsize=0,
                            **kwds)

@CheckHosts('hosts')
@MakeList(0)
def call_bash_capture_named_files(command,hosts=None,**kwds):
    """
    Call using the standard subprocess call along with a bash shell
    and capture stdout and stderr output into temporary file.

    **Arguments**:
      command : list of strings:
        A list of command arguments used by subprocess.Popen.
      hosts : list of hosts
        Used by decorator or as a dummy argument.
      **kwds :
        Keywords to pass to subprocess.Popen.

    **Returns**:
      subprocess.Popen :
        The subprocess.Popen object from calling the command.  The stdout_fh
         and stderr_fh attributes give the file handle to temporary files
         holding these outputs.
    """
    # TODO other shells?
    #      merge lists?
    stdout_fh = os.fdopen(tempfile.mkstemp()[0],'r+')
    stderr_fh = os.fdopen(tempfile.mkstemp()[0],'r+')
    p = subprocess.Popen(['bash','--login','-c'] + [' '.join(command)],
                         stdin=subprocess.PIPE,
                         stdout=stdout_fh,
                         stderr=stderr_fh,
                         bufsize=0,
                         **kwds)
    # can I add the named files to the Popen object?
    p.stdout_fh = stdout_fh
    p.stderr_fh = stderr_fh
    return p


def escape_path_pattern(path):
    """
    Escape patterns in a path in order to allow matching.

    **Arguments**:
      path : string
        The root path to find directories in.

    **Returns**:
      string
        The escaped pattern.
    """
    # Wow, can't use raw or re.escape to get results I want!
    new_path = path.replace('\\','\\\\')
    new_path = new_path.replace('.*','[^\\\/]*')
    new_path = new_path.replace('(','\(')
    new_path = new_path.replace(')','\)')
    return new_path

def strip_slashes(path):
    """
    Strip slashes of the beginning and end of a path.

    **Arguments**:
      path : string
        The path to strip slashes from.

    **Returns**:
      string:
        The new path.
    """
    path = path.strip('\\')
    path = path.strip('/')
    return path

######################################################
## General path and environment variable functionality

def collapse_backslashes(string):
    """
    Collapse multiple backslashes to just one backslash.

    **Arguments**:
      string : string
        The string to collapse backslashes in.

    **Returns**:
      string:
        The new string.
    """
    while True:
        new_string = re.sub(r'\\\\',r'\\',string)
        if string == new_string:
            return new_string
        else:
            string = new_string

def collapse_slashes(string):
    """
    Collapse multiple slashes to just one slash.

    **Arguments**:
      string : string
        The string to collapse slashes in.

    **Returns**:
      string:
        The new string.
    """
    while True:
        new_string = re.sub(r'//',r'/',string)
        if string == new_string:
            return new_string
        else:
            string = new_string

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
    new_path = os.path.expandvars(path)
    new_path = os.path.expanduser(new_path)
    return new_path

def makepath(path):
    """
    Recursively make a path if it does not exist.

    **Arguments**:
      path : string
        The path to check and make.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def join_path_list(path_list,delimeter=PATH_DELIMETER):
    """
    Join a list of paths using a delimiter.

    **Arguments**:
      path_list : list of strings
        The list of paths to join with the ''delimiter''.
      delimeter : string
        A single-character path delimeter.

    **Returns**:
      string:
        The path list joined together as a string.
    """
    # good idea!
    if type(path_list) == types.StringType:
        return path_list
    else:
        path_string = delimeter.join(path_list)
        return path_string

# TODO: more docs!!!
def read_posix_regexp(path):
    """Generally only converts those regexps that have been found to be needed."""
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
    if string == None:
        return ''
    else:
        return string.strip()

# TODO: improve how colors work in interactive functions
def yell(string):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if hasattr(module,'__file__') and module.__file__:
        sys.stderr.write("%s%s: %s%s%s\n" % (BRed,os.path.basename(module.__file__),Red,string,Color_Off))
    else:
        sys.stderr.write("%s%s: %s%s%s\n" % (BRed,'python',Red,string,Color_Off))

def warn(string):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if hasattr(module,'__file__') and module.__file__:
        sys.stderr.write("%s%s: %s%s%s\n" % (BYellow,os.path.basename(module.__file__),Yellow,string,Color_Off))
    else:
        sys.stderr.write("%s%s: %s%s%s\n" % (BYellow,'python',Yellow,string,Color_Off))

def msg(string):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if hasattr(module,'__file__') and module.__file__:
        sys.stderr.write("%s%s: %s%s%s\n" % (BGreen,os.path.basename(module.__file__),Green,string,Color_Off))
    else:
        sys.stderr.write("%s%s: %s%s%s\n" % (BGreen,'python',Green,string,Color_Off))

def h1(string):
    newstring = "==== %s ================================================================================" % string
    newstring = newstring[0:80]
    sys.stderr.write("%s%s%s%s\n" % (White,On_Blue,newstring,Color_Off))

def h2(string):
    newstring = "---- %s ------------------------------------------------------------" % string
    newstring = newstring[0:60]
    sys.stderr.write("%s%s%s%s\n" % (White,On_Purple,newstring,Color_Off))
