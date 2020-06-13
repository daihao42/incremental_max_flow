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
        self.parents = set()
        self.children = set()

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
        for i in self.elist:
            self.vdict[i.vid].parents.add(self.vdict[i.uid])
            self.vdict[i.uid].children.add(self.vdict[i.vid])

class BKTree():

    def __init__(self,vlist,elist):
        self.S = 's'
        self.T = 't'
        self.orphans = []
        self.frees = []
        self.g = Graph(vlist,elist)
        self.g.init_neighbor()
        self.vdict = self.g.vdict
        
    def init_tree(self):
        for i in self.vdict[self.S].children:
            i.parent = self.vdict[self.S]
            i.tree = self.S

        self.vdict[self.T].children.clear()
        for i in self.vdict[self.T].parents:
            i.parent = self.vdict[self.T]
            i.tree = self.T
            self.vdict[self.T].children.add(i)
            i.children,i.parents = i.parents,i.children
        self.vdict[self.T].parents.clear()

    def augment(self):
        

    def adopt(self):
        pass

if __name__ == '__main__':
    vlist = [Vertex("s"),Vertex("t"),Vertex("1"),Vertex("2"),Vertex("3"),Vertex("4")]
    elist = [Edge("s","4",11),Edge("4","1",6),Edge("1","2",8),Edge("2","t",7),Edge("1","t",2),Edge("3","t",8),Edge("2","4",1),Edge("2","3",6)]
    bktree = BKTree(vlist,elist)
    bktree.init_tree()
    for i in vlist:
        try:
            print(i.nid,[x.nid for x in i.parents],i.tree)
        except:
            continue
