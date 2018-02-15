        """
=======================================
cycle_finder.py
=======================================
Determines whether a graph G = (V,E) has a cycle of length k, and if it does, outputs one such cycle.
Given graph G = (V, E)
Key objects:
        
        1) F(i,j,p): family of sets of interior points of each path from vertex i to j of length p+1
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
        —apply Algorithm 1 to B(q,w,v,p) with T = L U {u}, label with output U {w}
Main algorithm:
        —F(i,j,0) is the empty set if {i,j} is in E and otherwise the empty family; B(k-1,i,j,0) is a tree with a single node labeled with the empty set in the former case and 'LAMBDA' in the latter
        —Apply Algorithm 2 to get B(k-2,i,j,1) for all i,j
        -Repeat, B(0,u,v,k-1) has singleton node labeled lambda if no path between u and v exists
        —otherwise, a path between u and v does exist and the label is its internal vertices

Example:

G = nx.Graph()
G.add_edges_from([(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,2),(2,4),(3,6),(3,8),(4,7),(4,8),(4,9),(5,9),(5,6),(6,9),(7,9),(8,9)])

Below we have the 3-tree for F(0,9,2)

T = nx.DiGraph()
T.add_edges_from([(frozenset({1, 6}), frozenset({8, 3}), {'label': 1}), (frozenset({1, 6}), frozenset({4, 7}), {'label': 6}), (frozenset({8, 3}), frozenset({2, 4}), {'label': 8}), (frozenset({8, 3}), frozenset({8, 4}), {'label': 3}), (frozenset({4, 7}), frozenset({1, 7}), {'label': 4}), (frozenset({4, 7}), frozenset({1, 5}), {'label': 7}), (frozenset({2, 4}), frozenset({3, 6}), {'label': 4}), (frozenset({2, 4}), frozenset({4, 7}), {'label': 2}), (frozenset({8, 4}), frozenset({2, 4}), {'label': 8}), (frozenset({8, 4}), 'LAMBDA', {'label': 4}), (frozenset({1, 7}), frozenset({1, 5}), {'label': 7}), (frozenset({1, 7}), frozenset({8, 3}), {'label': 1}), (frozenset({1, 5}), frozenset({2, 4}), {'label': 1}), (frozenset({1, 5}), frozenset({8, 3}), {'label': 5})])

T = nx.DiGraph()
T.add_edges_from([(0,1,{'weight': 1}), (0, 2, {'weight': 6}), (1,3, {'weight': 8}), (1, 4, {'weight': 3}), (2, 5, {'weight': 4}), (2, 6, {'weight': 7}), (3, 7, {'weight': 4}), (3, 8, {'weight': 2}), (4, 9, {'weight': 8}), (4, 10, {'weight': 4}), (5, 11, {'weight': 7}), (5,  12, {'weight': 1}), (6, 13, {'weight': 1}), (6, 14, {'weight': 5})])

dict = {0:frozenset({1, 6}), 1: frozenset({8, 3}), 2: frozenset({4, 7}), 3: frozenset({2, 4}), 4: frozenset({8, 4}), 5: frozenset({1, 7}), 6: frozenset({1, 5}), 7: frozenset({3, 6}), 8: frozenset({4, 7}), 9: frozenset({2, 4}), 10: 'LAMBDA', 11: frozenset({1, 5}), 12: frozenset({8, 3}), 13: frozenset({2, 4}), 14: frozenset({8, 3})}

nx.set_node_attributes(T, dict, 'label')

U = find_root(T)
K = {6,4,7}
disjoint_set(T, K, U)
frozenset({1, 5})

A simpler graph

G = nx.Graph()
G.add_edges_from([(0,1),(1,2),(0,2)])

Let's search for a path from 0 to 2 of length 2

B2010 = nx.DiGraph()
B2010.add_node(frozenset({0,1}))
B2020 = nx.DiGraph()
B2020.add_node('LAMBDA')
B2120 = nx.DiGraph()
B2120.add_node(frozenset({1,2}))

We compute

B1011 = nx.DiGraph()
B1011.add_node('LAMBDA')
B1021 = nx.DiGraph()
B1021.add_node('LAMBDA')
B1121 = nx.DiGraph()
B1121.add_node('LAMBDA')

Then

B0012 = nx.DiGraph()
B0012.add_node(frozenset({0,1}))
B0022 = nx.DiGraph()
B0022.add_node('LAMBDA')
B0122 = nx.DiGraph()
B0122.add_node(frozenset({1,2}))

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

def get_node_labels(graph, nodes, attribute):
  labels = [graph.nodes[x][attribute] for x in nodes]
  return labels

# The following function implements Algorithm 1
# Need to get the function to return instead of print
def disjoint_set(T, K, U):
  if U =='LAMBDA':
    return(U)
  elif not bool(U&K):
    return(U)
  else:
    children = [T.nodes[x]['label'] for x in T.neighbors(U)]
    while children != []:
      try:
        child = children.pop()
        if T[U][child]['label'] in K & U:
          U = child
          return disjoint_set(T, K, U)
      except KeyError:
        pass

def initial_tree_maker(G):
  # get basic structure of initial trees
  D = {}
  for x in itertools.product(*[G.nodes(),G.nodes]):
    D.update({x:nx.DiGraph()})
    if x in G.edges():
      D[x].add_node(frozenset({}))
    else:
      D[x].add_node('LAMBDA')
  return(D)

def initial_next_generation_node(G, D):
  P = {}
  for (u,v) in G.edges():
    B = nx.DiGraph()
    N = [x for x in G.neighbors(u) if x != v]
    if N == []:
      B.add_node('LAMBDA')
    else:
      w = N.pop()
      U = disjoint_set(D[(w,v)],{w},find_root(D[(w,v)]))
      B.add_node(U)
    P.update({(u,v):B})
  return(P)

def root_leaf(tree, root, leaf):
  H = set()
  H.update({leaf})
  p = list(tree.predecessors(leaf))
  if p != []:
    return(root_leaf(tree, root, p.pop()))
  else:
    return(H)


def next_generation(G, P):
  for (u,v) in G.edges():
    B = P[u,v]
    L = [x for x in B.nodes() if B.out_degree(x) == 0]
    root = find_root(B)
    for leaf in L:
      path = root_leaf(B,root, leaf)
    if N == []:
      B.add_node('LAMBDA')
    else:
      w = N.pop()
      U = disjoint_set(D[(w,v)],{w},find_root(D[(w,v)]))
      B.add_node(U)
    P.update({(u,v):B})
  return(P)



    D.update({x:nx.DiGraph()})
    D[x].add_node(frozenset)

  B = nx.DiGraph()
  D = {dictionary of trees}
  N = [x for x in list(G.neighbors(u)) if x != v]
  for w in N:
    U = disjoint_set(D[(w,v)],K,find_root(D[(w,v)]).pop())
      if U = 'LAMBDA':
        B.add_edges_from([(V,U)])



G = nx.Graph()
G.add_edges_from([(0,1),(1,2),(0,2)])

 = nx.DiGraph()
2010.add_node(frozenset({0,1}))

'2020' = nx.DiGraph()
2020.add_node('LAMBDA')

2120 = nx.DiGraph()
2120.add_node(frozenset({1,2}))

D = {(0,1):nx.DiGraph(),(0,2):nx.DiGraph(),(1,2): nx.DiGraph()}

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
                                                               
