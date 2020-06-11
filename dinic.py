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
        self.feasible = 0
        #self.residual = capacity
        self.lable = 0

    def rflow(self,flow,direction):
        self.uvfeasible = self.feasible + flow
        #self.residual = capacity - flow

    def setCapacity(self,nc):
        self.capacity = nc

    def setLabel(la):
        self.label = la
    
class Graph():
    def __init__(self,vlist,elist):
        self.vlist = vlist
        self.elist = elist

    def capGraph(self):
        eadj = {}
        for i in self.elist:
            eadj[i.uid+","+i.vid] = i
            eadj[i.vid+","+i.uid] = i
        return vlist,eadj

    def residualGraph(self):
        eadj = {}
        for i in self.elist:
            f_i = eadj[i.uid+","+i.vid].feasible
            if(f_i == 0):
                eadj[i.uid] = 
