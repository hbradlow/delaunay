import numpy as np
import math
import IPython

id = 0
def generate_id():
    global id
    id += 1
    return id

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
        self.id = generate_id()
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
    #dest 2d?
    return orient_2d(p,e.org(),e.dest())>0

def right_of(p,e):
    #dest 2d?
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
    def face_vertices(self):
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
        self.data = p1
        self.sym().data = p2
    def q_edge(self):
        return

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
    def all_edges(self,seen=None):
        if not seen:
            seen = set()
        seen.add(self.edges[0])
        for e in self.edges:
            if e.next not in seen:
                seen.add(e.next)
                for s in e.next.q.all_edges(seen):
                    seen.add(s)
        return seen
    def __repr__(self):
        return "Quad: " + str(self.id)
    def default_edge(self):
        return self.edges[0]
