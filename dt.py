from structures import Face, orient_2d, QuadEdge
import IPython

class Triangulation:
    def __init__(self):
        self.edges = []
        self.faces = []
    
    def locate(self,vertex):
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
