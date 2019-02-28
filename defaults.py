#!/usr/local/bin/sage -python
# -*- coding: iso-8859-15 -*-
"""."""
# DO NOT EDIT DIRECTLY IF NOT IN python-stdlib-personal, THIS FILE IS ORIGINALLY FROM https://github.com/akroshko/python-stdlib-personal

# Copyright (C) 2018, Andrew Kroshko, all rights reserved.
#
# Author: Andrew Kroshko
# Maintainer: Andrew Kroshko <akroshko.public+devel@gmail.com>
# Created: Thu Aug 09, 2018
# Version: 20190228
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

# configuration options
# TODO: put in seperate file

__all__= ['MAXUPDATESTRINGS','LIMITPERSEGMENT','CHECKDELAY','HOSTLIST','MAXREDUCTIONS','TYPICAL_CORES','NOMINAL_PARITIONS','WORKWAIT']
# tuning parameters to reduce load on database
# TODO: upgrade these to match machines after they are used

MAXUPDATESTRINGS=4096
LIMITPERSEGMENT=32768
# MAXUPDATESTRINGS=256
# LIMITPERSEGMENT=2048
# check the database every 3 seconds.... originally 10
CHECKDELAY=2
# for testing
# LIMITPERSEGMENT=128
# TODO: need a master hostlist, farm everything out if more than one hostlist?
HOSTLIST=['akroshko-main','akroshko-server']
# only reduce amount of work per chunk a certain number of times
MAXREDUCTIONS=2
# assign more work when number assigned is less than typical cores, to keep cores full even if some things take a long time
TYPICAL_CORES=4
# TODO: upped from 4 for better load balancing
NOMINAL_PARITIONS=16
# make hostname specific
# LIMITPERSEGMENT=2048
WORKWAIT=2
# memory is big so this is fine
# should have table I read to get...
# hostname (whether work is assigned to me)
# table name to go to
# solver name
