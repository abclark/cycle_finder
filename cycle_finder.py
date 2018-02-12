"""
=======================================
cycle_finder.py
=======================================
Determines whether a graph G = (V,E) has a cycle of length k, and if it does, outputs one such cycle.

Given graph G = (V, E)

Key objects:
        1) F(i,j,p): family of interior points of all paths from vertex i to j of length p
        2) B(q,i,j,p):
        —tree of height at most q
        —nodes labeled by elements of F(i,j,p) or a special symbol lambda
        —nodes have one successor for each element of their label
        —this edge is labeled with this element
        -nodes labeled with either an element of F(i,j,p) that is disjoint from the collection of edge labels leading to that node or, if no such element exists, lambda

Algorithm 1: given B(q,i,j,p), and (up to?) q vertices T, compute U in F(i,j,p) disjoint from T in O(p.q)
        —search in B(q,i,j,p) (whose collection of node labels q-representative of F(i,j,p), see Monien 1985)
Algorithm 2: Given B(q,i,j,p) for all i,j, compute B(q-1,u,v,p+1) in O(q.(p+1)^q.degree(u))
        —wish to label a node, let L denote edge labels leading to that node
        —search for edge (u,w) with w not in L
        —if none, label node lambda; otherwise,
        —apply Algorithm 1 to B(q,w,v,p) with T = L U {u}, label with output
Main algorithm:
        —F(i,j,0) is {i,j} if in E or empty, B(k-1,i,j,0) is the singleton node labeled {i,j} or lambda
        —Apply Algorithm 2 to get B(k-2,i,j,1) for all i,j
        -Repeat, B(0,u,v,k-1) has singleton node labeled lambda if no path between u and v exists
        —otherwise, a path between u and v does exist and the label is its internal vertices

Example:

>>> T = nx.DiGraph()
>>> T.add_edges_from([(frozenset({1, 6}), frozenset({8, 3}), {'label': 1}), (frozenset({1, 6}), frozenset({4, 7}), {'label': 6}), (frozenset({8, 3}), frozenset({2, 4}), {'label': 8}), (frozenset({8, 3}), frozenset({8, 4}), {'label': 3}), (frozenset({4, 7}), frozenset({1, 7}), {'label': 4}), (frozenset({4, 7}), frozenset({1, 5}), {'label': 7}), (frozenset({2, 4}), frozenset({3, 6}), {'label': 4}), (frozenset({2, 4}), frozenset({4, 7}), {'label': 2}), (frozenset({8, 4}), frozenset({2, 4}), {'label': 8}), (frozenset({8, 4}), 'LAMBDA', {'label': 4}), (frozenset({1, 7}), frozenset({1, 5}), {'label': 7}), (frozenset({1, 7}), frozenset({8, 3}), {'label': 1}), (frozenset({1, 5}), frozenset({2, 4}), {'label': 1}), (frozenset({1, 5}), frozenset({8, 3}), {'label': 5})])
>>> U = find_root(T)
>>> K = {6,4,7}
>>> disjoint_set(T, K, U)
frozenset({1, 5})
>>> 

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

# a function that finds the root of a tree
def find_root(tree):
  return([n for n,d in tree.in_degree() if d==0].pop())

# The following function implements Algorithm 1
# Need to get the function to return instead of print
def disjoint_set(T, K, U):
  if U =='LAMBDA':
    print(U)
  elif not bool(U&K):
    print(U)
  else:                    
    children = list(T.neighbors(U))
    while children != []:      
      try:
        child = children.pop()
        if T[U][child]['label'] in K & U:
          U = child
          disjoint_set(T, K, U)
      except KeyError:
        pass

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
