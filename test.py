from gui import Visualizer, Point2D, Line2D, Box2D, add_line, Polygon2D
import Tkinter as tk
from structures import Vertex, QuadEdge, Edge, Face, make_edge
from dt import Triangulation

import IPython

#initial setup
vertices = [Vertex(250,100),Vertex(100,200),Vertex(200,300),Vertex(500,100)]
faces = [Face(),Face()]
edges = [make_edge(vertices[0],vertices[1],left=faces[0]),make_edge(vertices[1],vertices[2],left=faces[0]),make_edge(vertices[0],vertices[2],left=faces[1],right=faces[0]),make_edge(vertices[2],vertices[3],left=faces[1]),make_edge(vertices[3],vertices[0],left=faces[1])]


dt = Triangulation()
dt.edges = edges
dt.faces = faces
dt.vertices = vertices

vertices_to_add = [Vertex(275,150),Vertex(175,180)]
#vertices_to_add = [Vertex(175,180)]

#commit = True
#for v in vertices_to_add:
#    dt.insert_site(v,commit=commit)


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
    f = dt.locate(v)
    draw_faces()
    if f:
        print f
        vis.add_drawable(Polygon2D(f.vertices()))
        for n in f.neighbors():
            vis.add_drawable(Polygon2D(n.vertices(),fill="blue"))
    draw_skeleton()

    vis.draw()

def click_callback(event):
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
