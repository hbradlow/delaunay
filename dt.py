from structures import Face, orient_2d
import IPython

class Triangulation:
    def __init__(self):
        self.edges = []
        self.faces = []
        self.vertices = []
    
    def locate(self,vertex):
        handle = self.edges[0].default_handle()
        while True:
            print handle
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

    def insert_site(self,vertex,commit=True):
        face = self.locate(vertex)
        conflicts = []
        frontier = [face]
        while frontier:
            f = frontier.pop()
            if f.incircle(vertex):
                conflicts.append(f)
                if not commit:
                    f.conflict=True
                for n in f.neighbors():
                    if n not in conflicts:
                        frontier.append(n)
        if not commit:
            self.vertices.append(vertex)
            return


        #TODO: handle the case where a point lies on another edge
        #if vertex == edge.origin or vertex == edge.destination:
        #    return # we already handled this vertex
        #elif edge.contains(vertex):
        #    pass

        vertices,first_face = self.merge_faces(conflicts)

        prev_face = face
        prev_vertex = None
        first_vertex = None
        try:
            for v in vertices:
                if not first_vertex:
                    first_vertex = v
                f = Face()
                e = make_edge(vertex,v,right=prev_face,left=f)
                self.edges.append(e)
                self.edges.append(e.get_reverse())
                self.faces.append(f)

                if prev_vertex:
                    e1 = v.get_edge(prev_vertex)
                    e2 = prev_vertex.get_edge(v)
                    e2.left = prev_face
                    e1.right = prev_face

                prev_face = f
                prev_vertex = v
            e1 = first_vertex.get_edge(prev_vertex)
            e2 = prev_vertex.get_edge(first_vertex)
            e2.left = prev_face
            e1.right = prev_face
        except:
            IPython.embed()

        self.vertices.append(vertex)
