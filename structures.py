import numpy as np
id = 0
def generate_id():
    global id
    id += 1
    return id

def make_edge(origin,destination,left=None,right=None):
    e1 = Edge(origin,destination,left,right)
    origin.add_edge(e1)
    if right and not right.edge:
        right.edge = e1

    e2 = Edge(destination,origin,right,left)
    destination.add_edge(e2)
    if left and not left.edge:
        left.edge = e1

    return e1

def incircle(a,b,c,d):
    def get_vector(p):
        return [p.x,p.y,p.x**2+p.y**2,1]
    m = np.array([get_vector(a),get_vector(b),get_vector(c),get_vector(d)])
    return np.linalg.det(m)>0

def orient_2d(p,q,r):
    """
        > 0 if CCW
        < 0 if CW
        = 0 if colinear
    """
    return (q.x-p.x)*(r.y-p.y) - (r.x-p.x)*(q.y-p.y)

class Vertex:
    def __init__(self,x,y,edges=None):
        self.x = x
        self.y = y
        self.edges = edges #outgoing edges
        if not edges:
            self.edges = []
        self.id = generate_id()
    def add_edge(self,edge):
        def edge_compare(e1,e2):
            return orient_2d(e1.destination,self,e2.destination)
        self.edges.append(edge)
        self.edges = sorted(self.edges,cmp=edge_compare)
    def get_edge(self,vertex):
        for edge in self.edges:
            if edge.destination == vertex:
                return edge
        return None
    def next_edge(self,edge):
        return self.edges[(self.edges.index(edge)+1)%len(self.edges)]
    def dual(self):
        return Face(self.edge)
    def __repr__(self):
        return "Vertex: " + str(self.id)

class QuadEdge:
    def __init__(self,e):
        self.edge = e
    def tail_next(self):
        return self.edge.origin.next_edge(self.edge)
    def flip(self):
        return Edge(self.edge.origin,self.edge.destination,left=self.edge.right,right=self.edge.left)
    def rotate(self):
        return Edge(self.edge.right,self.edge.left,left=self.edge.origin,right=self.edge.destination)

class Edge:
    def __init__(self,origin,destination,left=None,right=None):
        self.origin = origin
        self.destination = destination
        self.left = left
        self.right = right
        self.id = generate_id()

    def vertex_on_right(self,vertex):
        return orient_2d(self.origin,self.destination,vertex) <= 0

    def get_reverse(self):
        """
            The edge going the other direction between destination and origin
        """
        return self.destination.get_edge(self.origin)

    def next(self):
        """
            The next edge on the right face
        """
        return self.destination.next_edge(self.get_reverse())

    def __repr__(self):
        return "Edge: " + str(self.id)

class Face: #convex
    def __init__(self,edge=None):
        self.edge = edge
        self.id = generate_id()
    def neighbors(self):
        for edge in self.edges():
            if edge.right:
                yield edge.right
    def reverse_edges(self):
        """
            Return the edges of this face.
        """
        e = self.edge.get_reverse().next()
        while e != self.edge:
            yield e
            e = e.next()
    def vertices(self):
        for edge in self.edges():
            yield edge.origin
    def edges(self):
        """
            Return the edges of this face.
        """
        e = self.edge.next()
        while e != self.edge:
            yield e
            e = e.next()
        yield e
    def contains_vertex(self,v):
        for edge in self.edges():
            if not edge.vertex_on_right(v):
                return False
        return True
    def dual(self):
        #TODO fix
        return Vertex(0,0)
    def __repr__(self):
        return "Face: " + str(self.id)
