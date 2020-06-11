from nplot import graphPlot

__author__ = 'dai'

MAXVALUE = 65535

class Vertex():
    '''
    comp_cost = (compute_cost_at_edge,compute_cost_at_cloud)
    '''
    def __init__(self,nid,comp_cost,color='black',pre_edge=(False,False)):
        self.nid = nid
        self.comp_edge,self.comp_cloud = comp_cost
        self.color = color
        if(pre_edge[0]):
            self.is_edge = pre_edge[1]
        else:
            self.is_edge = self._isEdge()


    def _isEdge(self):
        if(self.comp_edge == -1):
            return False
        if(self.comp_cloud == -1):
            return True
        return True if(self.comp_edge < self.comp_cloud) else False

    def scalar_weight(self):
        return abs(self.comp_edge - self.comp_cloud)

class Edge():
    '''
    comm_cost = (communication_cost_same_side,communication_cost_different_side)
    '''
    def __init__(self,v1,v2,comm_cost,color='black',style='solid'):
        self.v1 = v1
        self.v2 = v2
        self.comm_w1,self.comm_w2 = comm_cost
        self.color = color
        self.style = style
    
    def scalar_weight(self):
        if(self.comm_w2 == -1):
            return MAXVALUE
        return self.comm_w2 - self.comm_w1

class Graph():
    def __init__(self,vertex_list,edge_list):
        self.vertex_list = vertex_list
        self.edge_list = edge_list

    def augment(self):
        cloud = Vertex("cloud",(0,0),"red",(True,False))
        edge = Vertex("edge",(0,0),"blue",(True,False))
        for v in self.vertex_list:
            if(v.is_edge):
                self.edge_list.append(Edge(edge,v,(0,v.scalar_weight()),'blue','dashed'))
            else:
                self.edge_list.append(Edge(cloud,v,(0,v.scalar_weight()),'red','dashed'))
        self.vertex_list.extend([cloud,edge])
        return self.vertex_list,self.edge_list

if __name__ == '__main__':
    pass

