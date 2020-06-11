'''
__author__ = 'dai'
'''

class Vertex():
    def __init__(self,nid):
        self.nid = nid
        self.status_active = "active"
        self.status_passive = "passive"
        self.status = self.status_active
        self.tree = None
        self.parent = None
        self.neighbors = []

class Edge():
    def __init__(self,uid,vid,capacity):
        self.uid = uid
        self.vid = vid
        self.capacity = capacity

class Graph():
    def __init__(self,vlist,elist):
        self.vdict = {}
        self.elist = elist
        for i in vlist:
            self.vdict[i.nid] = i

    def init_neighbor(self):
        for i in elist:
            [self.uid]


class BKTree():

    def __init__(self,elist,vlist):
        self.S = 's'
        self.T = 't'
        self.orphans = []
        self.frees = []
        self.g = Graph(vlist,elist)
        

    def init_tree(self):
        pass

    def augment(self):
        pass

    def adopt(self):
        pass



