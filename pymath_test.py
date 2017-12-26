#!/usr/bin/python
import os,sys
from pymath_common import *
pymath_default_imports(globals(),locals())

# TODO: allows multiple labels at start
tic('fullthing')
tic()
tic('justpp')
pp({'z':['1','2','3','4','5','6','7','8','9','10'],
    'y':['1','2','3','4','5','6','7','8','9','10']})
toc('justpp')
time.sleep(1)
toc()
time.sleep(1)
toc('fullthing')
