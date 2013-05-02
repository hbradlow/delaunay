import math

id = 0
def generate_id():
    global id
    id += 1
    return id

from itertools import product, islice
def det(M,prod=1):
    dim = len(M)
    if dim == 1:
        return prod * M.pop().pop()
    it = product(xrange(1,dim),repeat=2)
    prod *= M[0][0]
    return det([[M[x][y]-M[x][0]*(M[0][y]/M[0][0]) for x,y in islice(it,dim-1)] for i in xrange(dim-1)],prod)

def incircle(a,b,c,d):
    def get_vector(p):
        return [p.x,p.y,p.x**2+p.y**2,1]
    m = [get_vector(a),get_vector(b),get_vector(c),get_vector(d)]
    return det(m)>0

def orient_2d(p,q,r):
    """
        > 0 if CCW
        < 0 if CW
        = 0 if colinear
    """
    return (q.x-p.x)*(r.y-p.y) - (r.x-p.x)*(q.y-p.y)

class Vertex:
    def __init__(self,x,y,edges=None,index=None,containing_face=None):
        self.x = x
        self.y = y
        self.index = index
        self.id = generate_id()
        self.containing_face = containing_face
    def distance_to(self,v):
        return math.sqrt((self.x-v.x)**2 + (self.y-v.y)**2)
    def __repr__(self):
        return "Vertex: " + str(self.id) + "(" + str(self.x) + "," + str(self.y) + ")"

def make_edge():
    q = QuadEdge()
    return q.default_edge()

def splice(a,b):
    alpha = a.o_next().rot()
    beta = b.o_next().rot()
    t1 = b.o_next()
    t2 = a.o_next()
    t3 = beta.o_next()
    t4 = alpha.o_next()

    a.next = t1
    b.next = t2
    alpha.next = t3
    beta.next = t4

def delete_edge(e):
    splice(e,e.o_prev())
    splice(e.sym(),e.sym().o_prev())
    #TODO: remove e from memory

def connect(a,b):
    e = make_edge()
    splice(e,a.l_next())
    splice(e.sym(),b)
    e.end_points(a.dest(),b.org())
    return e

def swap(e):
    a = e.o_prev()
    b = e.sym().o_prev()
    splice(e,a)
    splice(e.sym(),b)
    splice(e,a.l_next())
    splice(e.sym(),b.l_next())
    e.end_points(a.dest(),b.dest())

def left_of(p,e):
    return orient_2d(p,e.org(),e.dest())<0

def right_of(p,e):
    return orient_2d(p,e.dest(),e.org())>0

def on_edge(x,e):
    #TODO
    epsilon = .1
    t1 = x.distance_to(e.org())
    t2 = x.distance_to(e.dest())
    if t1<epsilon or t2<epsilon:
        return True
    t3 = e.org().distance_to(e.dest())
    if t1>t3 or t2>t3:
        return False

    return False

class Edge:
    def __init__(self,q):
        self.q = q
        self.num = 0
        self.next = None
        self.data = None
        self.id = generate_id()
    def neighbors(self):
        """
            Returns the neighboring faces of the face definated by this edge.
        """
        fv = [self]
        e = self.l_prev()
        while e!=self:
            fv.append(e)
            e = e.l_prev()

        if self.o_prev() not in fv:
            yield self.o_prev()
        e = self.l_prev()
        while e!=self:
            if e.o_prev() not in fv:
                yield e.o_prev()
            e = e.l_prev()
    def contains_vertex(self,v):
        for edge in self.face_edges():
            if right_of(v,edge):
                return False
        return True
    def offer_vertices(self,vertices):
        if not self.rot().data:
            self.rot().data = [] #clear the vertices
        remaining = []
        for vertex in vertices:
            if self.contains_vertex(vertex):
                self.rot().data.append(vertex)
                vertex.containing_face = self
            else:
                remaining.append(vertex)
        for edge in self.face_edges():
            edge.rot().data = self.rot().data
        return remaining
    def vertex_chain(self):
        """
            The edges that all have self.org() as their origin.
        """
        l = [self]
        e = self.o_next()
        while e != self:
            l.append(e)
            e = e.o_next()
        return l
    def print_face(self):
        for edge in self.face_edges():
            print edge.org(),",",edge.dest()
    def face_edges(self):
        """
            The edges around the face that is defined by this edge.
        """
        yield self
        e = self.l_prev()
        while e!=self:
            yield e
            e = e.l_prev()
    def face_vertices(self):
        """
            The vertices around the face that is defined by this edge.
        """
        yield self.data
        e = self.l_prev()
        while e!=self:
            yield e.data
            e = e.l_prev()
    def __repr__(self):
        return "Edge: " + str(self.id) + " (" + str(self.q) + ")"
    def rot(self):
        return self.q.edges[(self.num+1)%4]
    def invrot(self):
        return self.q.edges[(self.num-1)%4]
    def sym(self):
        return self.q.edges[(self.num+2)%4]
    def o_next(self):
        return self.next
    def o_prev(self):
        return self.rot().o_next().rot()
    def d_next(self):
        return self.sym().o_next().sym()
    def d_prev(self):
        return self.invrot().o_next().invrot()
    def l_next(self):
        return self.invrot().o_next().rot()
    def l_prev(self):
        return self.o_next().sym()
    def r_next(self):
        return self.rot().o_next().invrot()
    def r_prev(self):
        return self.sym().o_next()
    def org(self):
        return self.data
    def dest(self):
        return self.sym().org()
    def end_points(self,p1,p2):
        """
            Set the endpoints of this edge.
        """
        self.data = p1
        self.sym().data = p2

class QuadEdge:
    def __init__(self):
        self.edges = [Edge(self),Edge(self),Edge(self),Edge(self)]
        self.edges[0].num = 0
        self.edges[1].num = 1
        self.edges[2].num = 2
        self.edges[3].num = 3

        self.edges[0].next = self.edges[0]
        self.edges[1].next = self.edges[3]
        self.edges[2].next = self.edges[2]
        self.edges[3].next = self.edges[1]

        self.id = generate_id()
    def __repr__(self): return "Quad: " + str(self.id)
    def default_edge(self):
        return self.edges[0]
