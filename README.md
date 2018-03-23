# cycle_finder
       
              
<p>Contents<br>       
  <a href="#Installation">Installation</a><br>
  <a href="#Basic usage">Basic usage</a><br>
  <a href="#Mathematical background">Mathematical background</a><br>
  <a href="#API">API</a><br>


<h2 id="Installation">Installation</h2>
        
Download <code>cycle_finder.py</code>
        
<h2 id="Basic usage">Basic usage</h2>
        
<pre><code>import networkx as nx
from cycle_finder import path_finder

# Create a directed graph

G = nx.DiGraph()
G.add_edges_from([(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,2),(2,4),(3,6),(3,8),(4,7),(4,8),(4,9),(5,6),(5,9),(6,9),(7,9),(8,9)])

Z = path_finder(G,length_of_path)
</code></pre>
        
<h2 id="Mathematical background">Mathematical background</h2>
       
<p>See <a href="https://abclark.github.io/notes/Monien85.pdf">Monien 1985</a>.</p>

<h2 id="API">API</h2>
        
 <pre><code>>>> import networkx as nx
>>> from cycle_finder import path_finder
>>> G = nx.DiGraph()
>>> G.add_edges_from([(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,2),(2,4),(3,6),(3,8),(4,7),(4,8),(4,9),(5,6),(5,9),(6,9),(7,9),(8,9)])
>>> Z = path_finder(G,5)
>>> Z[0,9].nodes(data=True)
NodeDataView({1: {'label': {1, 2, 4, 7}}})
>>> </code></pre>

<p>The output of <code>path_finder(G,k)</code> is a dictionary of directed graphs, indexed by paire of nodes <code>u,v</code>, and each consisting of a single vertex. The vertex is labelled <code>'LAMBDA'</code> if and only if there is no path of length  <code>k</code> from <code>u</code> to <code>v</code>; otherwise it is labelled with the internal vertices of such a path.</p>

