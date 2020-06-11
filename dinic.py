'''
__author__ = 'dai'
'''

class Vertex():
    def __init__(self,nid):
        self.nid = nid

class Edge():
    def __init__(self,uid,vid,capacity):
        self.uid = uid
        self.vid = vid
        self.capacity = capacity
        self.residual = capacity
        self.inverseResidual = 0
        self.lable = 0

    def rFlow(self,feasible_flow):
        self.residual = self.residual - feasible_flow
        self.inverseResidual = self.inverseResidual + feasible_flow

    def inverseRFlow(self,feasible_flow):
        self.residual = self.residual + feasible_flow
        self.inverseResidual = self.inverseResidual - feasible_flow

    def setCapacity(self,nc):
        self.capacity = nc

    def setLabel(la):
        self.label = la
    
class Graph():
    def __init__(self,vlist,elist):
        self.vdict = {}
        self.elist = elist
        for i in vlist:
            self.vdict[i.nid] = i

    def capGraph(self):
        eadj = {}
        for i in self.elist:
            eadj[i.uid+","+i.vid] = i
        return self.vdict,eadj

    def residualGraph(self):
        eadj = {}
        for i in self.elist:
            c_i = i.residual
            if(c_i != 0):
                eadj[i.uid+","+i.vid] = c_i
            i_c_i = i.inverseResidual
            if(i_c_i != 0):
                eadj[i.vid+","+i.uid] = i_c_i
        return self.vdict,eadj

class Dinic():
    def __init__(self,elist,vdict):
        self.S = 's'
        self.T = 't'
        self.elist = elist
        self.vdict = vdict

    def _bfs(self,vlist,layers,eadj):
        layer = []
        for i in layers[-1]:
            for j in vlist:
                if(eadj.get(i+","+j) != None):
                    layer.append(j)
        layers.append(layer)
        for i in layer:
            vlist.remove(i)
        return layers,vlist

    def _dfs(self,layers,eadj):
        # once dfs needn't update the inverse flow
        paths = []
        current = 0
        lnext = 1
        while True:
            for i in layers[current]:
                paths.append(i)
                for j in layers[lnext]:
                    if((eadj.get(i+","+j) != None) and (eadj.get(i+","+j) != 0)):
                        layer.append(j)
                        current = current + 1
                        break

                if((current == lnext) and (current < len(layers) - 1)):
                    lnext = lnext + 1
                    break
                if(current == len(layers) - 1):
                    paths.pop()
                    current = current - 1
                else if 
            if(paths[-1] == self.T):
                break
        return paths

    def LayerNetwork(self,eadj):
        layers = []
        layers.append([self.S])
        vlist = list(self.vdict.keys())
        vlist.remove(self.S)
        while(len(vlist) != 0):
            layers,vlist = self._bfs(vlist,layers,eadj)
        return layers

    
if __name__ == '__main__':
    vlist = [Vertex("s"),Vertex("t"),Vertex("1"),Vertex("2"),Vertex("3"),Vertex("4")]
    elist = [Edge("s","4",11),Edge("4","1",6),Edge("1","2",8),Edge("2","t",7),Edge("1","t",2),Edge("3","t",8),Edge("2","4",1),Edge("2","3",6)]
    g = Graph(vlist,elist)
    vdict,eadj = g.residualGraph()
    dinic = Dinic(elist,vdict)
    print(dinic.LayerNetwork(eadj))

