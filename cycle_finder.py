"""
=======================================
cycle_finder.py                    
=======================================
Determines whether a graph G = (V,E) has a cycle of length 2k, and if it does, outputs one cuch cyc
le. 
"""

#: The current version of this package.
__version__ = '0.0.1-dev'

import networkx as nx
import numpy as np
import copy
import itertools
import math
import sys
from pprint import pprint

#global things
tolerance = np.finfo(np.float).eps*10e10
