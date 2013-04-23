import numpy as np

id = 0
def generate_id():
    global id
    id += 1
    return id

def incircle(a,b,c,d):
    def get_vector(p):
        return [p.x,p.y,p.x**2+p.y**2,1]
    m = np.array([get_vector(a),get_vector(b),get_vector(c),get_vector(d)])
    return np.linalg.det(m)<0

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
        self.id = generate_id()
    def __repr__(self):
        return "Vertex: " + str(self.id)

class Handle:
    def __init__(self,edge,orientation):
        self.edge = edge
        self.orientation = orientation
    def destination(self):
        #TODO: fix
        if self.orientation != 2:
            return self.edge.destination
        else:
            return self.edge.origin
    def origin(self):
        #TODO: fix
        if self.orientation != 2:
            return self.edge.origin
        else:
            return self.edge.destination
    def has_face(self):
        return self.f_next()
    def face_vertices(self):
        for handle in self.face_handles():
            yield handle.origin()
    def face_handles(self,seen=None):
        if not seen:
            seen = []
        if self.origin() not in seen:
            yield self
            seen.append(self.origin())
            for handle in self.f_next().face_handles(seen=seen):
                yield handle
    def right_of(self,vertex):
        return orient_2d(self.origin(),self.destination(),vertex) < 0
    def f_next(self):
        """
            The next point along a face.
            First to o_next then flip it.
        """
        return self.sym().o_next()
    def o_next(self):
        edge = self.edge.links[self.orientation]
        if edge:
            if edge.origin == self.edge.origin:
                return edge.default_handle()
            else:
                return edge.default_handle().sym()
        return None
    def d_prev(self):
        return self.invrot().o_next().invrot()
    def sym(self):
        o = (self.orientation+2)%4
        return Handle(self.edge,o)
    def invrot(self):
        o = (self.orientation+3)%4
        return Handle(self.edge,o)
    def rot(self):
        o = (self.orientation+1)%4
        return Handle(self.edge,o)
    def __repr__(self):
        return "Handle: (" + str(self.edge) + ", " + str(self.orientation) + ")"

class QuadEdge:
    def __init__(self,origin,destination):
        self.origin = origin
        self.destination = destination
        self.links = [None,None,None,None]
        self.id = generate_id()
    def default_handle(self):
        return Handle(self,2)
    def __repr__(self):
        return "QuadEdge: " + str(self.id)

class Face: #convex
    def __init__(self,edge=None):
        self.edge = edge
        self.conflict = False
        self.id = generate_id()
    def merge_with(self,other):
        for edge in self.edges():
            edge.left = other
            edge.get_reverse().right = other
    def neighbors(self):
        """
            Returns a generator for the neighbors of this face.
        """
        for edge in self.edges():
            if edge.right:
                yield edge.right
    def reverse_edges(self):
        """
            Return a generator for the reversed edges of this face.
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
            Return a generator for the edges of this face.
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
    def incircle(self,vertex):
        g = self.vertices()
        #use three consecutive points on the face
        a = next(g)
        b = next(g)
        c = next(g)
        return incircle(a,b,c,vertex)
    def dual(self):
        #TODO fix
        return Vertex(0,0)
    def __repr__(self):
        return "Face: " + str(self.id)
