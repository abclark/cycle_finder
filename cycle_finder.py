"""
=======================================
cycle_finder.py
=======================================
Determines whether a graph G = (V,E) has a cycle of length 2k, and if it does, outputs one cuch cycle.
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

# given node in tree, disjoint set compares node and its decendents with set until it finds a node
# who is disjoint from set
def disjoint_set(tree,set,node):
  if bool(node & set) = False:
    return(node)
  elseif node & set = {lambda}:
    return(lambda)
  else:
    for sonedge, son node in sons:
      disjoint_set(tree, set, sonnode)

# iterate through nodes of tree, finding a U that is disjoint from set
# or concluding that no such set exists
def disjoint_set_finder(tree, set)
  for node in nodesoftree:
    if disjoint_set(tree, set, node) != lambda:
      return disjoint_set(tree, set, node)
    else:
      return lambda

def tree_maker(tree_list_indexed_by_edges, set):
  tree = {}
  # start at level i node, having constructed the tree to level i-1
  # collect in a set E the edge labels from root to node
  # label node as disjoint_set(tree,E,)
