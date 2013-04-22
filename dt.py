from structures import Face, Edge, make_edge

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

    def insert_site(self,vertex):
        face = self.locate(vertex)

        #TODO: handle the case where a point lies on another edge
        #if vertex == edge.origin or vertex == edge.destination:
        #    return # we already handled this vertex
        #elif edge.contains(vertex):
        #    pass

        prev_face = face
        prev_vertex = None
        first_vertex = None
        for v in face.vertices():
            if not first_vertex:
                first_vertex = v
            f = Face()
            self.edges.append(make_edge(vertex,v,left=prev_face,right=f))
            self.faces.append(f)

            if prev_vertex:
                e1 = v.get_edge(prev_vertex)
                e2 = prev_vertex.get_edge(v)
                e1.left = f
                e2.right = f

            prev_face = f
            prev_vertex = v

        e1 = prev_vertex.get_edge(first_vertex)
        e2 = first_vertex.get_edge(prev_vertex)
        e1.left = f
        e2.right = f

        self.vertices.append(vertex)
