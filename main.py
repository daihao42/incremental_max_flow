import networkx as nx
from models import Vertex,Edge,Graph
from nplot import graphPlot
#from networkx.algorithms.connectivity import minimum_st_edge_cut,minimum_st_node_cut
#from networkx.algorithms.flow import shortest_augmenting_path

def networkxPackage(vl,el):
    G = nx.Graph()
    for v in vl:
        G.add_node(v.nid,color = v.color)
    for e in el:
        G.add_edge(e.v1.nid,e.v2.nid,capacity=e.scalar_weight(), weight=e.scalar_weight(),color=e.color,style=e.style)
    return G

def min_cut(G):
    return nx.minimum_cut(G,_s='edge',_t='cloud')

def filter_nodes(nodes):
    def inner(n):
        return n in nodes
    return inner

if __name__ == '__main__':
    vl = [Vertex("1",(4,2)),Vertex("2",(8,1)),Vertex("3",(11,3)),Vertex("4",(0,11))]
    el = [Edge(vl[1-1],vl[2-1],(4,12)),Edge(vl[2-1],vl[3-1],(9,15)),Edge(vl[2-1],vl[4-1],(6,7)),Edge(vl[4-1],vl[1-1],(7,13))]
    g = Graph(vl,el)
    avl,ael = g.augment()
    G = networkxPackage(avl,ael)
    graphPlot(G)
    # minimum cut
    snodes,tnodes = min_cut(G)[1]
    # filter node 
    sf = filter_nodes(snodes)
    tf = filter_nodes(tnodes)
    graphPlot(nx.subgraph_view(G,filter_node=tf))

