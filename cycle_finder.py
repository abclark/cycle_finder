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

def disjoint_set(T, K, starting_node):
  labels = nx.get_node_attributes(T, 'label')
  U = set(labels[starting_node])
  if U =={'LAMBDA'}:
    return(U)
  elif not bool(set(U)&K):
    return(U)
  else:
    children = list(T.neighbors(starting_node))
    while children != []:
      try:
        child = children.pop()
        if T[starting_node][child]['weight'] in K & U:
          starting_node = child
          return disjoint_set(T, K, starting_node)
      except KeyError:
        pass

def initial_tree_maker(G):
  # get basic structure of initial trees
  D = {}
  for x in itertools.product(*[G.nodes(),G.nodes]):
    D.update({x:nx.DiGraph()})
    if x in G.edges():
      D[x].add_node(1, label = {})
    else:
      D[x].add_node(1, label = {'LAMBDA'})
  return(D)

def initial_tree_dictionary(G):
  D = {}
  for x in itertools.product(*[G.nodes(),G.nodes]):
    D.update({x:nx.DiGraph()})
  return(D)


def root_leaf_edge_set(tree, starting_node, leaf):
  H = set()
  while leaf != starting_node:
    e = tree[[*tree.predecessors(leaf)].pop()][leaf]['weight']
    H.update({e})
    leaf = [*tree.predecessors(leaf)].pop()
  return(H)

def find_root(tree):
  return([n for n,d in tree.in_degree() if d==0].pop())


T = nx.DiGraph()

T.add_nodes_from([(1, {'label': {1,6}} ), (11, {'label' : {3,8}} ), (12, {'label': {4,7} }), (111, {'label': {2,4}}), (112, {'label' : {4,8}}), (121, {'label' : {1,7}}), (122, {'label' : {1,5} }), (1111, {'label' : {3,6}}), (1112, {'label' : {4,7}}), (1121, {'label': {2,4}}), (1122, {'label': 'LAMBDA'}), (1211, {'label': {1,5}}), (1212, {'label': {3,8}}), (1221, {'label': {2,4}}), (1222, {'label': {3,8}}) ] )

T.add_edges_from([(1, 11, {'weight': 1}), (1, 12, {'weight': 6}), (11, 111, {'weight': 8}), (11, 112, {'weight': 3}), (12, 121, {'weight': 4}), (12, 122, {'weight': 7}), (111, 1111, {'weight': 4}), (111, 1112, {'weight': 2}), (112, 1121, {'weight': 8}), (112, 1122, {'weight': 4}), (121, 1211 , {'weight': 7}), (121, 1212, {'weight': 1}), (122, 1221, {'weight': 1}), (122, 1222, {'weight': 5})])

def next_generation(G, P, K, q):
  # G is the graph
  # P is the previous generation of trees
  # K is the current generation of trees
  R = copy.deepcopy(K)
  for (u,v) in set(itertools.product(*[G.nodes(),G.nodes])):
    N = [x for x in G.neighbors(u) if x != v]
    # if N is the empty list, move to next index (u,v)
    if N == []:
      R[(u,v)].add_nodes_from([(1 ,{'label': {'LAMBDA'}})])
    else:
      w = N.pop()
      L = [x for x in R[(u,v)].nodes() if R[(u,v)].out_degree(x) == 0]
      # if L is the empty list, don't compute edge set and label root
      if len(L) == 0:
        U = disjoint_set(P[(w,v)], {u}, 1)
        # if U is 'LAMBDA' there is no path from w to v
        if U == {'LAMBDA'}:
           R[(u,v)].add_nodes_from([(1 ,{'label': {'LAMBDA'}})])
        else:
           U.update({w})
           R[(u,v)].add_nodes_from([(1,{'label': U})])
      else:
        # if L is not the empty list, compute path from root to leaf
        labels = nx.get_node_attributes(R[(u,v)], 'label')
        for leaf in L:
        # if leaf is LAMBDA we can move to the next leaf
          if leaf != {'LAMBDA'}:
            path = root_leaf_edge_set(R[(u,v)], 1, leaf)
            # if depth is q we can move to next leaf
            if len(path) < q:
              E = path & {u}
              for i,z in list(enumerate(labels[leaf])):
                U = disjoint_set(P[(w,v)], E, 1)
                if U == {'LAMBDA'}:
                  j = i + 1
                  R[(u,v)].add_nodes_from([(int(str(leaf) + str(j)), {'label': {'LAMBDA'}})])
                  R[(u,v)].add_edges_from([(leaf, int(str(leaf) + str(j)), {'weight': z})])
                elif z == w:
                  j = i + 1
                  R[(u,v)].add_nodes_from([(int(str(leaf) + str(j)), {'label': {'LAMBDA'}})])
                  R[(u,v)].add_edges_from([(leaf, int(str(leaf) + str(j)), {'weight': z})])
                else:
                  j = i + 1
                  U.update({w})
                  R[(u,v)].add_nodes_from([(int(str(leaf) + str(j)), {'label': U})])
                  R[(u,v)].add_edges_from([(leaf, int(str(leaf) + str(j)), {'weight': z})])
  return(R)

                                                               
