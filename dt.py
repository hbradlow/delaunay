from structures import *
import IPython

class Triangulation:
    def __init__(self,a,b,c,fast_locate=False):
        edge_a = make_edge()
        edge_a.end_points(a,b)

        edge_b = make_edge()
        splice(edge_a.sym(),edge_b)
        edge_b.end_points(b,c)

        edge_c = make_edge()
        splice(edge_b.sym(),edge_c)
        edge_c.end_points(c,a)

        splice(edge_c.sym(),edge_a)

        self.edges = [edge_a,edge_b,edge_c]
        self.bounds = [edge_a,edge_b,edge_c]
        self.bound_points = [a,b,c]
        self.faces = []

        self.fast_locate = fast_locate
    
    def initial_edge(self):
        if self.edges:
            return self.edges[0]
        return None

    def get_edges(self):
        output = set()
        l = set([self.initial_edge(),self.initial_edge().sym()])
        while l:
            e = l.pop()
            output.add(e)
            for i in [e.next,e.next.sym()]:
                if i not in output:
                    l.add(i)
        return output

    def get_triangles(self):
        triangles = []
        seen = set()
        for e in self.get_edges():
            if e in seen:
                continue
            l = list(reversed([v for v in e.face_vertices()]))
            if None not in l and len(l)==3:
                triangles.append(l)
                for i in e.face_edges():
                    seen.add(i)
        return triangles

    def conflict_locate(self,x,safe=False,limit=10):
        return x.containing_face
    def locate(self,x,safe=False,limit=10):
        """
            Walking algorithm to locate the vertex.
        """
        e = self.initial_edge()
        i = 1
        while True and (not safe or i<limit):
            i += 1
            if x == e.org() or x == e.dest():
                return e
            elif right_of(x,e):
                e = e.sym()
            elif not right_of(x,e.o_next()):
                e = e.o_next()
            elif not right_of(x,e.d_prev()):
                e = e.d_prev()
            else:
                return e
    def remove_bounds(self):
        """
            Remove the triangles that were created from the initial triangle.
        """
        edges = set()
        for e in self.edges:
            if e.org() in self.bound_points or e.dest() in self.bound_points:
                edges.add(e)
        for edge in edges:
            if edge in self.edges:
                delete_edge(edge)
                self.edges.remove(edge)
    def insert_site(self,x):
        """
            Insert a point into this triangulation. Taken from the paper.
        """
        if self.fast_locate:
            e = self.conflict_locate(x)
            vertex_set = e.rot().data
        else:
            e = self.locate(x)

        #TODO: include this
        """
        if x == e.org() or x == e.dest():
            return
        elif on_edge(x,e):
            e = e.o_prev()
            delete_edge(e.o_next())
        """

        base = make_edge()
        initial_edge = base.sym()
        self.edges.append(base)

        base.end_points(e.org(),x)
        splice(base,e)
        start = base

        while True:
            base = connect(e,base.sym())
            self.edges.append(base)
            e = base.o_prev()
            if e.l_next() == start:
                break

        if self.fast_locate:
            for edge in initial_edge.vertex_chain():
                vertex_set = edge.offer_vertices(vertex_set)

        while True:
            t = e.o_prev()
            if right_of(t.dest(),e) and incircle(e.org(),t.dest(),e.dest(),x):
                if self.fast_locate:
                    vertex_set = e.rot().data + e.sym().rot().data
                swap(e)
                if self.fast_locate:
                    vertex_set = e.sym().offer_vertices(vertex_set)
                    vertex_set = e.offer_vertices(vertex_set)
                e = e.o_prev()
            elif e.o_next() == start:
                return
            else:
                e = e.o_next().l_prev()
