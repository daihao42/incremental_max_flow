'''
__author__ = 'dai'
'''
from functools import reduce

class Vertex():
    def __init__(self,nid):
        self.nid = nid

class Edge():
    def __init__(self,uid,vid,capacity):
        self.uid = uid
        self.vid = vid
        self.capacity = capacity
        self.residual = capacity
        # directed
        #self.inverseResidual = 0
        # undireted
        self.inverseResidual = capacity
        self.lable = 0

    def rFlow(self,feasible_flow):
        self.residual = self.residual - feasible_flow
        self.inverseResidual = self.inverseResidual + feasible_flow

    def inverseRFlow(self,feasible_flow):
        self.residual = self.residual + feasible_flow
        self.inverseResidual = self.inverseResidual - feasible_flow

    def setCapacity(self,nc):
        self.capacity = nc

    def increaseCapacity(self,cap):
        self.residual = self.residual + cap
        self.inverseResidual = self.inverseResidual + cap
        self.capacity = self.capacity + cap

    def decreaseCapacity(self,cap):
        self.residual = self.residual - cap
        self.inverseResidual = self.inverseResidual - cap
        self.capacity = self.capacity - cap

class Graph():
    def __init__(self,vlist,elist):
        self.elist = elist
        self.vlist = vlist
        self._updateVDict()

    def addEdge(self,e):
        self.elist.append(e)

    def delEdge(self,e):
        self.elist.remove(e)

    def _updateVDict(self):
        self.vdict = {}
        for i in self.vlist:
            self.vdict[i.nid] = i

    def addVertex(self,v):
        self.vlist.append(v)
        self._updateVDict()

    def delVertex(self,nid):
        v = self.vdict.get(nid)
        self.vlist.remove(v)
        self._updateVDict()

    def capGraph(self):
        eadj = {}
        for i in self.elist:
            eadj[i.uid+","+i.vid] = i
        return self.vdict,eadj

    def residualGraph(self):
        eadj = {}
        edge_dict = {}
        for i in self.elist:
            c_i = i.residual
            if(c_i != 0):
                eadj[i.uid+","+i.vid] = c_i
            i_c_i = i.inverseResidual
            if(i_c_i != 0):
                eadj[i.vid+","+i.uid] = i_c_i
            edge_dict[i.uid+","+i.vid] = i
        return self.vdict,eadj,edge_dict

class Dinic():
    def __init__(self,vlist,elist):
        self.S = 's'
        self.T = 't'
        self.elist = elist
        self.vlist = vlist
        self.g = Graph(vlist,elist)
        self.vdict,self.eadj,self.edge_dict = self.g.residualGraph()

    def _dfs(self,layers,eadj,root,target,current = 1,paths=None):
        # once dfs needn't update the inverse flow
        if(current == len(layers)):
            return None
        for i in layers[current]:
            if((eadj.get(root+","+i) != None) and (eadj.get(root+","+i) != 0)):
                if(i == target):
                    paths = []
                    paths.append(i)
                    return paths

                paths = self._dfs(layers,eadj,i,target,current + 1,paths)
                if(paths != None):
                    paths.append(i)
                    return paths
        return paths

    def LayerNetwork(self,root):
        layers = []
        layers.append([root])
        vdict,eadj,edge_dict = self.g.residualGraph()
        vlist = list(vdict.keys())
        vlist.remove(root)
        ## BFS
        while(len(layers[-1]) != 0):
            layer = []
            for i in layers[-1]:
                for j in vlist:
                    if(eadj.get(i+","+j) != None):
                        layer.append(j)
            layer = list(set(layer))
            [vlist.remove(x) for x in layer]
            layers.append(layer)
        return layers[:-1]
    
    def _augmentOncePaths(self,layers):
        vdict,eadj,edge_dict = self.g.residualGraph()
        #layers = self.LayerNetwork(eadj)
        augmentpath = self._dfs(layers,eadj,self.S,self.T)
        while(augmentpath != None):
            augmentpath.append(self.S)
            augmentpath = augmentpath[::-1]

            edges = []
            inverse_edges = []
            edges_flow = []
            #print("augmentpath:",augmentpath)
            for i in range(len(augmentpath) - 1):
                e = edge_dict.get(augmentpath[i]+","+augmentpath[i+1])
                if(e != None):
                    edges.append(e)
                e = edge_dict.get(augmentpath[i+1]+","+augmentpath[i])
                if(e != None):
                    inverse_edges.append(e)

                edges_flow.append(eadj.get(augmentpath[i]+","+augmentpath[i+1]))
            #print("edges_flow",edges_flow)
            minflow = reduce(lambda x,y:min(x,y),edges_flow)
            #print(minflow)
            for i in edges:
                i.rFlow(minflow)
            for i in inverse_edges:
                i.inverseRFlow(minflow)
            vdict,eadj,edge_dict = self.g.residualGraph()
            #print(eadj)

            augmentpath = self._dfs(layers,eadj,self.S,self.T)

    '''
        return: min-cut sets S_set and T_set
    '''
    def Augment(self):
        vdict,eadj,edge_dict = self.g.residualGraph()
        vlist = list(vdict.keys())
        v_size = len(vlist)
        layers = self.LayerNetwork(self.S)
        layers_size = sum([len(x) for x in layers])
        while(layers_size == v_size):
            self._augmentOncePaths(layers)
            layers = self.LayerNetwork(self.S)
            layers_size = sum([len(x) for x in layers])
        self.S_set = reduce(lambda x,y:x+y,layers)
        self.T_set = list(set(vlist)^set(self.S_set))
        return self.S_set,self.T_set

    def increaseCapacity(self,uid,vid,cap):
        vdict,eadj,edge_dict = self.g.residualGraph()
        edge = edge_dict.get(uid+","+vid) if(edge_dict.get(uid+","+vid)!= None) else edge_dict.get(vid+","+uid)
        if((edge.residual != 0) and (edge.inverseResidual != 0)):
            edge.increaseCapacity(cap)
        else:
            edge.increaseCapacity(cap)
            self.S_set,self.T_set = self.Augment()

        return self.S_set,self.T_set

    def decreaseCapacity(self,uid,vid,cap):
        vdict,eadj,edge_dict = self.g.residualGraph()
        edge = edge_dict.get(uid+","+vid) if(edge_dict.get(uid+","+vid)!= None) else edge_dict.get(vid+","+uid)
        if((edge.residual >= cap) and (edge.inverseResidual >= cap)):
            edge.decreaseCapacity(cap)

        elif(edge.residual < cap):
            self._inverseAugmentPaths(edge.uid,edge.vid,cap-edge.residual)
            edge.decreaseCapacity(cap)

        elif(edge.inverseResidual < cap):
            self._inverseAugmentPaths(edge.vid,edge.uid,cap-edge.inverseResidual)
            edge.decreaseCapacity(cap)

        else:
            pass

        self.S_set,self.T_set = self.Augment()
        return self.S_set,self.T_set

    def _inverseAugmentPaths(self,u,v,cap):
        while(cap > 0):
            vdict,eadj,edge_dict = self.g.residualGraph()
            # try to remove u,v in eadj for optimaize runtime, TO-DO
            if(u == self.S):
                uspath = []
            else:
                uspath = self._dfs(self.LayerNetwork(u),eadj,u,self.S)
            #print("layers-"+u+":",self.LayerNetwork(u))
            #print(eadj)
            #print(eadj["3,4"],eadj["4,s"])
            uspath.append(u)
            uspath = uspath[::-1]
            #print("uspath:",u,uspath)

            if(v == self.T):
                tvpath = []
            else:
                tvpath = self._dfs(self.LayerNetwork(self.T),eadj,self.T,v)
            #print("tvpath:",tvpath)
            tvpath.append(self.T)
            tvpath = tvpath[::-1]

            augmentpath = tvpath + uspath
            eadj[v+","+u] = cap

            # adjust residual graph
            edges = []
            inverse_edges = []
            edges_flow = []
            for i in range(len(augmentpath) - 1):
                e = edge_dict.get(augmentpath[i]+","+augmentpath[i+1])
                if(e != None):
                    edges.append(e)
                e = edge_dict.get(augmentpath[i+1]+","+augmentpath[i])
                if(e != None):
                    inverse_edges.append(e)

                edges_flow.append(eadj.get(augmentpath[i]+","+augmentpath[i+1]))
            minflow = reduce(lambda x,y:min(x,y),edges_flow)
            for i in edges:
                i.rFlow(minflow)
            for i in inverse_edges:
                i.inverseRFlow(minflow)

            # minus minflow to adjust the cap
            cap = cap - minflow


    def addEdge(self,uid,vid,cap):
        e = Edge(uid,vid,cap)
        self.g.addEdge(e)
        # uid and vid are not in the same set
        if(not(set(self.S_set).issuperset({uid,vid}) or set(self.T_set).issuperset({uid,vid}))):
            self.S_set,self.T_set = self.Augment()
        return self.S_set,self.T_set

    def delEdge(self,uid,vid):
        vdict,eadj,edge_dict = self.g.residualGraph()
        edge = edge_dict.get(uid+","+vid) if(edge_dict.get(uid+","+vid)!= None) else edge_dict.get(vid+","+uid)
        self.S_set,self.T_set = self.decreaseCapacity(uid,vid,edge.capacity)
        self.g.delEdge(edge)
        return self.S_set,self.T_set

    def _checkEdgeSTSet(self,edges):
        Flag = False
        for i in edges:
            if(not(set(self.S_set).issuperset({i.uid,i.vid}) or set(self.T_set).issuperset({i.uid,i.vid}))):
                Flag = True
        return Flag

    def addVertex(self,nid,edges):
        v = Vertex(nid)
        edges = [Edge(u,v,c) for u,v,c in edges]
        for i in edges:
            self.g.addEdge(i)
        self.g.addVertex(v)
        # edge across S_set and T_set, need to re-min-cut
        if(self._checkEdgeSTSet(edges)):
            self.S_set,self.T_set = self.Augment()
        return self.S_set,self.T_set

    def _findEdges(self,nid):
        import re
        vdict,eadj,edge_dict = self.g.residualGraph()
        edges = []
        for k,v in edge_dict.items():
            if((re.match(f"^{nid},",k) or re.match(f",{nid}$",k))):
                edges.append(v)
        return edges

    def delVertex(self,nid):
        edges = self._findEdges(nid)
        for e in edges:
            self.delEdge(e.uid,e.vid)
        self.g.delVertex(nid)
        return self.S_set,self.T_set
               
if __name__ == '__main__':
    vlist = [Vertex("s"),Vertex("t"),Vertex("1"),Vertex("2"),Vertex("3"),Vertex("4")]
    elist = [Edge("s","4",11),Edge("4","1",6),Edge("1","2",8),Edge("2","t",7),Edge("1","t",2),Edge("3","t",8),Edge("2","4",1),Edge("2","3",6)]
    dinic = Dinic(vlist,elist)
    print(dinic.Augment())
    print(dinic.increaseCapacity("4","1",5))
    #print(dinic.increaseCapacity("s","4",5))
    _,eadj1,_ = dinic.g.residualGraph()
    #print(eadj1)
    print(dinic.decreaseCapacity("4","1",5))
    _,eadj2,_ = dinic.g.residualGraph()
    #print(dinic.addEdge("4","3",5))
    #print(dinic.g.residualGraph())
    #print(dinic.delEdge("t","3"))
    print(dinic.addVertex("5",[("4","5",4),("3","5",1)]))
    print(dinic.delVertex("5"))

    vlist2 = [Vertex("s"),Vertex("t"),Vertex("1"),Vertex("2"),Vertex("3"),Vertex("4")]
    elist2 = [Edge("s","4",11),Edge("4","1",6),Edge("1","2",8),Edge("2","t",7),Edge("1","t",2),Edge("3","t",8),Edge("2","4",1),Edge("2","3",6)]
    dinic2 = Dinic(vlist2,elist2)
    print(dinic2.Augment())
    _,eadj3,_ = dinic2.g.residualGraph()

    print(eadj2)
    print(eadj3)
    print(eadj2 == eadj3)
    #print(dinic.g.residualGraph())

