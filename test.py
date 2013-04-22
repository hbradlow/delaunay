from gui import Visualizer, Point2D, Line2D, Box2D, add_line, Polygon2D
import Tkinter as tk
from structures import Vertex, QuadEdge, Edge, Face, make_edge
from dt import Triangulation

import IPython

#initial setup
vertices = [Vertex(250,100),Vertex(100,200),Vertex(200,300),Vertex(500,100)]
faces = [Face(),Face()]
edges = [make_edge(vertices[0],vertices[1],left=faces[0]),make_edge(vertices[1],vertices[2],left=faces[0]),make_edge(vertices[0],vertices[2],left=faces[1],right=faces[0]),make_edge(vertices[2],vertices[3],left=faces[1]),make_edge(vertices[3],vertices[0],left=faces[1])]

print edges

dt = Triangulation()
dt.edges = edges
dt.faces = faces
dt.vertices = vertices

vertices_to_add = [Vertex(275,150),Vertex(175,180)]
#vertices_to_add = [Vertex(175,180)]
for v in vertices_to_add:
    dt.insert_site(v)


root = tk.Tk()

def add_stuff():
    for v in dt.vertices:
        vis.add_drawable(Point2D(v))
    for edge in dt.edges:
        vis.add_drawable(Line2D(edge.origin,edge.destination))

def mouse_callback(event):
    vis.clear()
    v = Vertex(event.x,event.y)
    f = dt.locate(v)
    if f:
        vis.add_drawable(Polygon2D(f.vertices()))
        for n in f.neighbors():
            vis.add_drawable(Polygon2D(n.vertices(),fill="blue"))

    add_stuff()
    vis.draw()

vis = Visualizer(root,800,600,mouse_callback=mouse_callback)
add_stuff()
vis.run()
root.mainloop()
