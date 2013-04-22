from structures import Face, Edge, make_edge, sort_vertices_around

class Triangulation:
    def __init__(self):
        self.edges = []
        self.faces = []
        self.vertices = []
    
    def locate(self,vertex):
        for face in self.faces:
            if face.contains_vertex(vertex):
                return face
        return None

    def merge_faces(self,faces):
        edges = []
        first_face = None
        for face in faces:
            if not first_face:
                first_face = face
            for edge in list(face.edges()):
                if edge in edges or edge.get_reverse() in edges:
                    face.merge_with(edge.left)

                    if edge in self.edges:
                        self.edges.remove(edge)
                    if edge.get_reverse() in self.edges:
                        self.edges.remove(edge.get_reverse())

                    edge.remove()
                    edge.get_reverse().remove()

                    first_face.edge = face.edge
                    self.faces.remove(face)
                edges.append(edge)
        return first_face.vertices()

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

        vertices = self.merge_faces(conflicts)

        prev_face = face
        prev_vertex = None
        first_vertex = None
        for v in vertices:
            if not first_vertex:
                first_vertex = v
            f = Face()
            self.edges.append(make_edge(vertex,v,right=prev_face,left=f))
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

        self.vertices.append(vertex)
