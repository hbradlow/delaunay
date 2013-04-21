id = 0
def generate_id():
    global id
    id += 1
    return id

class Vertex:
    def __init__(self,x,y,edges=[]):
        self.x = x
        self.y = y
        self.edges = edges #outgoing edges
        self.id = generate_id()
    def add_edge(self,edge):
        #TODO, sort edges by ccw order
        self.edges.append(edge)
    def next_edge(self,edge):
        return self.edges[(self.edges.index(edge)+1)%len(edges)]
    def dual(self):
        return Face(self.edge)
    def __repr__(self):
        return "Vertex: " + str(self.id)

class QuadEdge:
    def __init__(self,e):
        self.edge = e
        #self.sym = self.edge.get_reverse()
        #self.rot = Edge(self.edge.right.dual(),self.edge.left.dual(),self.edge.origin.dual(),self.edge.destination.dual())
        #self.invrot = Edge(self.edge.left.dual(),self.edge.right.dual(),self.edge.destination.dual(),self.edge.origin.dual())
    def next(self):
        return self.edge.origin.next_edge(self.edge)
    def flip(self):
        return Edge(self.edge.origin,self.edge.destination,left=self.edge.right,right=self.edge.left)
    def rotate(self):
        return Edge(self.edge.right,self.edge.left,left=self.edge.origin,right=self.edge.destination)

class Edge:
    def __init__(self,origin,destination,left=None,right=None):
        self.origin = origin
        self.desination = destination
        self.left = left
        self.right = right
        self.id = generate_id()

    def get_reverse(self):
        return Edge(self.destination,self.origin,self.right,self.left)

    def __repr__(self):
        return "Edge: " + str(self.id)

class Face:
    def __init__(self,edge=None):
        self.edge = edge
        self.id = generate_id()
    def dual(self):
        #TODO fix
        return Vertex(0,0)
    def __repr__(self):
        return "Face: " + str(self.id)
