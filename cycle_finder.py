        """
=======================================
cycle_finder.py
=======================================
Given a directed graph G = (V,E), find_paths(G,k) computes whether there is a simple path (a path that does not repeat any nodes) between any two nodes u and v.  

find_paths(G,k) is a dictionary of directed graphs, indexed by pairs of nodes u,v, each directed graph consisting of a single labelled root node. 

This root node is labelled with 'LAMBDA' if and only if there is no path of length k from node u to v; 
otherwise the label is the the internal nodes of one such a path. 

For example, in the following there is a path of length 5 between nodes 0 and 9, 
however there is no path of length 6 between these two nodes

>>> import networkx as nx
>>> from cycle_finder import path_finder
>>> G = nx.DiGraph()
>>> G.add_edges_from([(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,2),(2,4),(3,6),(3,8),(4,7),(4,8),(4,9),(5,6),(5,9),(6,9),(7,9),(8,9)])
>>> Z = find_paths(G,5)
>>> Z[0,9].nodes(data=True)
NodeDataView({1: {'label': {1, 2, 4, 7}}})
>>> Z = find_paths(G,6)
>>> Z[0,9].nodes(data=True)
NodeDataView({1: {'label': {'LAMBDA'}}})

The algorithm is an implementation of Monien 1985: 'How to find long paths efficiently'

Copyright 2017 Aubrey Clark.

cycle_finder is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.
"""

#: The current version of this package.
__version__ = '0.0.1-dev'

import networkx as nx
import numpy as np
import copy
import itertools
import math
import sys

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
      L = [x for x in R[(u,v)].nodes() if R[(u,v)].out_degree(x) == 0]
      # if L is the empty list, don't compute edge set and label root
      if len(L) == 0:
        [U,w] = key_step(N, P, {u}, v)
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
          if labels[leaf] != {'LAMBDA'}:
            path = root_leaf_edge_set(R[(u,v)], 1, leaf)
            # if depth is q we can move to next leaf
            if len(path) < q:
              for i,z in list(enumerate(labels[leaf])):
                E = path | {u} | {z}
                [U,w] = key_step(N, P, E, v)
                if U == {'LAMBDA'}:
                  j = i + 1
                  R[(u,v)].add_nodes_from([(int(str(leaf) + str(j)), {'label': {'LAMBDA'}})])
                  R[(u,v)].add_edges_from([(leaf, int(str(leaf) + str(j)), {'weight': z})])
                else: 
                  j = i + 1
                  V = U | {w}
                  R[(u,v)].add_nodes_from([(int(str(leaf) + str(j)), {'label': V})])
                  R[(u,v)].add_edges_from([(leaf, int(str(leaf) + str(j)), {'weight': z})])
  return(R)
  
def key_step(N, P, E, v):
  for w in N:
    U = disjoint_set(P[(w,v)], E, 1)
    if U != {'LAMBDA'}:
      if w not in E:
        return([U,w])
  return([{'LAMBDA'},w])
                                                               

 def generation(G,P,q):
  A[-1] = initial_tree_dictionary(G)
  for i in range(q+1):
    A[i] = next_generation(G, P, A[i-1], q)
  return(A[q])
   
def find_paths(G,k):
  B[-1] = initial_tree_maker(G)
  for j in range(k-1):
    B[j] = generation(G,B[j-1],k-j-2)
  return(B[k-2])       
        
