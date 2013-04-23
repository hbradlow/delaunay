from gui import Visualizer, Point2D, Line2D, Box2D, add_line, Polygon2D
import Tkinter as tk
from structures import Vertex, QuadEdge, Face
from dt import Triangulation

import IPython

#initial setup
vertices = [Vertex(250,100),Vertex(100,200),Vertex(200,300),Vertex(500,100)]
edges = []
edges.append(QuadEdge(vertices[0],vertices[1]))
edges.append(QuadEdge(vertices[1],vertices[2]))
edges.append(QuadEdge(vertices[2],vertices[3]))
edges.append(QuadEdge(vertices[3],vertices[0]))
edges.append(QuadEdge(vertices[0],vertices[2]))
edges[0].links = [None,edges[1],edges[4],None]
edges[1].links = [None,edges[4],edges[0],None]
edges[2].links = [None,edges[3],edges[4],None]
edges[3].links = [None,edges[4],edges[2],None]
edges[4].links = [edges[1],edges[2],edges[3],edges[0]]

vertices_to_add = [Vertex(275,150),Vertex(175,180)]

dt = Triangulation()
dt.edges = edges
dt.vertices = vertices

root = tk.Tk()

def draw_faces():
    for face in dt.faces:
        if face.conflict:
            vis.add_drawable(Polygon2D(face.vertices(),fill="green"))
def draw_skeleton():
    for edge in dt.edges:
        vis.add_drawable(Line2D(edge.origin,edge.destination))
    for v in dt.vertices:
        vis.add_drawable(Point2D(v))

def key_callback(event):
    dt.insert_site(vertices_to_add.pop())
    draw_faces()
    draw_skeleton()
    vis.draw()

def mouse_callback(event):
    vis.clear()
    v = Vertex(event.x,event.y)
    handle = dt.locate(v)
    if handle.sym().has_face():
        vis.add_drawable(Polygon2D(handle.sym().face_vertices(),fill="red"))
        for h in handle.sym().face_handles():
            hs = h.sym()
            if hs.has_face():
                vis.add_drawable(Polygon2D(hs.face_vertices(),fill="blue"))
    else:
        print "No face"
    draw_skeleton()
    vis.draw()

def click_callback(event):
    return
    v = Vertex(event.x,event.y)
    if dt.locate(v):
        dt.insert_site(v)
    vis.clear()
    draw_faces()
    draw_skeleton()
    vis.draw()

vis = Visualizer(root,800,600,key_callback=key_callback,mouse_callback=mouse_callback,click_callback=click_callback)
draw_faces()
draw_skeleton()
vis.run()
root.mainloop()
