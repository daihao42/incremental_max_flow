import networkx as nx
import pylab as plt

def graphPlot(G):

    edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])

    edge_colors = [d['color'] for u,v,d in G.edges(data=True)]
    edge_styles = [d['style'] for u,v,d in G.edges(data=True)]

    vertex_colors = [d['color'] for v,d in G.nodes(data=True)]

    #elist = [(u, v) for (u, v, d) in G.edges(data=True) ]

    pos = nx.spring_layout(G)#获取结点的位置,每次点的位置都是随机的

    nx.draw_networkx_edge_labels(G, pos, font_size=15, font_family='sans-serif', edge_labels=edge_labels)#绘制图中边的权重

    nx.draw_networkx_edges(G, pos, width=2, edge_color=edge_colors, style=edge_styles)

    # node label
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif',font_color="white")

    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=vertex_colors, with_labels=True)

    #nx.draw(G,pos,node_color=vertex_colors, node_size=800)

    plt.show()

if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge('A', 'B', weight=4)
    G.add_edge('B', 'D', weight=2)
    G.add_edge('A', 'C', weight=3)
    G.add_edge('C', 'D', weight=5)
    G.add_edge('A', 'D', weight=10)

    fixed_position = {'A':[ 0.55072989,  0.00426975], 'B': [ 1.,  0.], 'D': [ 0.38252302,  0.10520343], 'C': [ 0.,0.09481996]}#每个点在坐标轴中的位置

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] >= 5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] < 5]

    edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])

    pos = nx.spring_layout(G,pos = fixed_position)#获取结点的位置,每次点的位置都是随机的
    # draw edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2,edge_color='black', style='solid')
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style='dashed')

    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)#绘制图中边的权重

    # draw nodes
    nx.draw_networkx_nodes(G,pos,node_size=100,node_color='r')

    plt.show()
