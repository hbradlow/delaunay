from structures import *
import IPython

class Triangulation:
    def __init__(self,a,b,c):
        ea = make_edge()
        ea.end_points(a,b)

        eb = make_edge()
        splice(ea.sym(),eb)
        eb.end_points(b,c)

        ec = make_edge()
        splice(eb.sym(),ec)
        ec.end_points(c,a)

        splice(ec.sym(),ea)

        self.edges = [ea,eb,ec]
        self.faces = []
    
    def initial_edge(self):
        if self.edges:
            return self.edges[0]
        return None
    
    def locate(self,x):
        e = self.initial_edge()
        while True:
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
    def locate_old(self,vertex):
        handle = self.edges[0].default_handle()
        while True:
            if vertex == handle.origin() or vertex == handle.destination():
                return handle
            elif handle.right_of(vertex):
                handle = handle.sym()
            elif handle.o_next() and not handle.o_next().right_of(vertex):
                handle = handle.o_next()
            elif handle.d_prev() and not handle.d_prev().right_of(vertex):
                handle = handle.d_prev()
            else:
                return handle
    def insert_site(x):
        e = self.locate(x)
        if x == e.org() or x == e.dest():
            return
        elif on_edge(x,e):
            e = e.o_prev()
            delete_edge(e.o_next())

        base = make_edge()
        base.end_points(e.org(),x)
        splice(base,e)
        start = base

        while e.l_next() != start:
            base = connect(e,base.sym())
            e = base.o_prev()

        while True:
            t = e.o_prev()
            if right_of(t.dest(),e) and in_circle(e.org(),t.dest(),e.dest(),x):
                swap(e)
                e = e.o_prev()
            elif e.o_next() == start:
                return
            else:
                e = e.o_next().l_prev()

    def merge_faces(self,faces):
        edges = []
        duplicates = []
        first_face = None
        for face in faces:
            if not first_face:
                first_face = face
            for edge in list(face.edges()):
                if edge in edges or edge.get_reverse() in edges:
                    duplicates.append(edge)

                    face.merge_with(edge.left)

                    if edge in self.edges:
                        self.edges.remove(edge)
                    if edge.get_reverse() in self.edges:
                        self.edges.remove(edge.get_reverse())

                    if edge in edges:
                        edges.remove(edge)
                    if edge.get_reverse() in edges:
                        edges.remove(edge.get_reverse())

                    edge.remove()
                    edge.get_reverse().remove()

                    for new_edge in edges:
                        if new_edge not in duplicates:
                            first_face.edge = new_edge
                            break
                    if face in self.faces:
                        self.faces.remove(face)
                else:
                    edges.append(edge)
        return first_face.vertices(), first_face

    def insert_site_old(self,vertex,commit=True):
        handle = self.locate(vertex)

        #TODO: handle the case where a point lies on another edge
        #if vertex == edge.origin or vertex == edge.destination:
        #    return # we already handled this vertex
        #elif edge.contains(vertex):
        #    pass

        #add new edges
        prev_handle = None
        for h in [a for a in handle.sym().face_handles()]:
            e = QuadEdge(vertex,h.origin())
            e.default_handle().sym().splice_with(h)
            print e
            print h.f_next()
            print e.default_handle().f_next()
            self.edges.append(e)

            if prev_handle:
                prev_handle.splice_with(e.default_handle())
            prev_handle = e.default_handle()

        self.vertices.append(vertex)
