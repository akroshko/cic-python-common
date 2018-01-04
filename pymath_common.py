#!/usr/bin/env python
"""A standard set of utility and system administration functions."""
# DO NOT EDIT DIRECTLY IF NOT IN python-stdlib-personal, THIS FILE IS ORIGINALLY FROM https://github.com/akroshko/python-stdlib-personal

# Copyright (C) 2015-2018, Andrew Kroshko, all rights reserved.
#
# Author: Andrew Kroshko
# Maintainer: Andrew Kroshko <akroshko@gmail.com>
# Created: Wed Nov 15, 2017
# Version: 20180103
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
import time

TICTOCLABELS={}

__all__ = ['All']

class All(object):
    """ Provide a decorator that add a class or method to the __all__ variable. """
    def __init__(self,global_dict):
        self.global_dict = global_dict

    def __call__(self,obj):
        if not self.global_dict.has_key('__all__'):
            self.global_dict['__all__'] = []
        self.global_dict['__all__'].append(obj.__name__)
        return obj

def pymath_import_module(theglobals,thelocals,module_name,module_as,submodule=None):
    if submodule==None:
        themodule = __import__(module_name,theglobals,thelocals)
        theglobals[module_as] = themodule
    else:
        themodule = __import__(module_name,theglobals,thelocals,[submodule])
        theglobals[module_as] = getattr(themodule,submodule)

@All(globals())
def tic(label=None):
    global TICTOCLABELS
    if label == None:
        TICTOCLABELS['default'] = time.time()
    else:
        TICTOCLABELS[label] = time.time()

# TODO: use a file-local label
@All(globals())
def toc(label=None):
    if label == None:
        thetime = time.time() - TICTOCLABELS['default']
        print ("Timing default: %.2fs" % thetime)
    else:
        thetime = time.time() - TICTOCLABELS[label]
        print "Timing " + label + (": %.2fs" % thetime)

@All(globals())
def filter_list_of_tuples_invalid(list_of_tuples):
    """Filter out in invalid values.  This generally for plotting, so
things that are unplottable like None are filtered out.
TODO: nan and inf?
      raise special exception if non-scalar too?"""
    return [t for t in list_of_tuples if t[0] is not None and t[1] is not None]

# TODO: possibily work with tuples
@All(globals())
def make_axis_symlog_y(ax,ythresh,xmin,xmax,ymin,ymax):
    if ymin < -ythresh or ymax > ythresh:
        print "Setting symlog with ", ythresh
        ax.set_yscale('symlog',linthreshy=ythresh)
        if ymax > ythresh:
            print "Top symlog"
            ax.hlines(ythresh,xmin,xmax,color='r')
        if ymin < -ythresh:
            print "Bottom symlog"
            ax.hlines(-ythresh,xmin,xmax,color='r')

@All(globals())
def pymath_default_imports(theglobals,thelocals):
    # TODO: don't need to return anything yet
    pymath_import_module(theglobals,thelocals,'copy','copy')
    pymath_import_module(theglobals,thelocals,'os','os')
    # TODO: from pprint import pprint
    pymath_import_module(theglobals,thelocals,'pprint','pprint')
    pymath_import_module(theglobals,thelocals,'pprint','pp',submodule='pprint')
    # TODO: import a nice re matcher
    pymath_import_module(theglobals,thelocals,'random','random')
    pymath_import_module(theglobals,thelocals,'re','re')
    pymath_import_module(theglobals,thelocals,'socket','socket')
    pymath_import_module(theglobals,thelocals,'datetime','datetime')
    pymath_import_module(theglobals,thelocals,'pycurl','pycurl')
    pymath_import_module(theglobals,thelocals,'time','time')
    pymath_import_module(theglobals,thelocals,'traceback','traceback')
    pymath_import_module(theglobals,thelocals,'urllib','urllib')
    pymath_import_module(theglobals,thelocals,'math','m')
    pymath_import_module(theglobals,thelocals,'Queue','Queue')
    pymath_import_module(theglobals,thelocals,'lxml','lxml')
    # TODO: lxml.html
    pymath_import_module(theglobals,thelocals,'json','json')
    pymath_import_module(theglobals,thelocals,'re','re')
    pymath_import_module(theglobals,thelocals,'subprocess','subprocess')
    pymath_import_module(theglobals,thelocals,'multiprocessing','multiprocessing')
    pymath_import_module(theglobals,thelocals,'multiprocessing','Pool',submodule='Pool')
    pymath_import_module(theglobals,thelocals,'psycopg2','psycopg2')
    # TODO: psycopg2.extras
    pymath_import_module(theglobals,thelocals,'numpy','np')
    pymath_import_module(theglobals,thelocals,'scipy','sp')
    pymath_import_module(theglobals,thelocals,'matplotlib','mpl')
    # XXXX: this allows things to be done with no graphics
    # TODO: have a nicer configuration that accomodates headless servers, but still allows graphics to pop up
    theglobals['mpl'].use('Agg')
    pymath_import_module(theglobals,thelocals,'matplotlib','plt',submodule='pyplot')

    # from matplotlib.backends.backend_pdf import PdfPages

# TODO: move pymath_default_imports_and_open_database in here

################################################################################
## some array utilities

@All(globals())
def compact_array_print(arr):
    # TODO: string are immutable, this is not efficient...
    thestring = ""
    # TODO: do not use a for loop, make something that works well with various boolean things
    # TODO: have something that gives relative magnitude (logarithmic too)
    for i in xrange(arr.shape[1]):
        for j in xrange(arr.shape[0]):
            if arr[i,j] > 0.5:
                thestring += '##'
            else:
                thestring += '..'
        thestring += '\n'
    return thestring
