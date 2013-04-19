id = 0
def generate_id():
    global id
    id += 1
    return id

class Vertex:
    def __init__(self,x,y,edge=None):
        self.x = x
        self.y = y
        self.edge = edge
        self.id = generate_id()
    def __repr__(self):
        return "Vertex: " + str(self.id)

class Edge:
    def __init__(self,origin,destination,left=None,right=None):
        self.origin = origin
        self.desination = destination
        self.left = left
        self.right = right
        self.id = generate_id()
    def __repr__(self):
        return "Edge: " + str(self.id)

class Face:
    def __init__(self,edge=None):
        self.edge = edge
        self.id = generate_id()
    def __repr__(self):
        return "Face: " + str(self.id)
