# cycle_finder

This is Python code implementing the algorithm of [Monien 1985](Monien1985.pdf) for finding paths in a directed graph. It computes for each pair of nodes whether a simple path of a specified length exists between them, and if so returns its interior nodes.</p>
              
<p>Contents<br>       
  <a href="#Installation">Installation</a><br>
  <a href="#Basic usage">Basic usage</a><br>
  <a href="#Mathematical background">Mathematical background</a><br>
  <a href="#API">API</a><br>


<h2 id="Installation">Installation</h2>
        
Download <code>cycle_finder.py</code>
        
<h2 id="Basic usage">Basic usage</h2>
        
<pre><code>import networkx as nx
from cycle_finder import find_paths

# Create a directed graph

G = nx.DiGraph()
G.add_edges_from([(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,2),(2,4),(3,6),(3,8),(4,7),(4,8),(4,9),(5,6),(5,9),(6,9),(7,9),(8,9)])

Z = find_paths(G,length_of_path)
</code></pre>
        
<h2 id="Mathematical background">Mathematical background</h2>
       
<p>See [Monien 1985](Monien1985.pdf).</p>

<h2 id="API">API</h2>
        
 <pre><code>>>> import networkx as nx
>>> from cycle_finder import find_paths
>>> G = nx.DiGraph()
>>> G.add_edges_from([(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,2),(2,4),(3,6),(3,8),(4,7),(4,8),(4,9),(5,6),(5,9),(6,9),(7,9),(8,9)])
>>> Z = find_paths(G,5)
>>> Z[0,9].nodes(data=True)
NodeDataView({1: {'label': {1, 2, 4, 7}}})
>>> Z = find_paths(G,6)
>>> Z[0,9].nodes(data=True)
NodeDataView({1: {'label': {'LAMBDA'}}})
>>> </code></pre>

<p>The output of <code>find_paths(G,k)</code> is a dictionary of directed graphs indexed by pairs of nodes <code>u,v</code>. Each directed graph consists of a single node, labelled <code>'LAMBDA'</code> if there is no simple path of length <code>k</code> from node <code>u</code> to <code>v</code> and otherwise labelled with the internal nodes of one such path.</p>

<p>Above, there is a path of length <code>5</code> between nodes <code>0</code> and <code>9</code>, but no path of length <code>6</code>.</p>
