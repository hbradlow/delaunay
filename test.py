from gui import Visualizer, Point2D, Line2D, Box2D, add_line, Polygon2D
import Tkinter as tk
from structures import *
from dt import Triangulation
import threading

from parse import load_node

lock = threading.Lock()

import IPython

#initial setup
vertices = load_node("spiral.node")
min_x = min(vertices,key=lambda v: v.x).x
min_y = min(vertices,key=lambda v: v.y).y
max_x = max(vertices,key=lambda v: v.x).x
max_y = max(vertices,key=lambda v: v.y).y

dx = max_x-min_x
dy = max_y-min_y

v1 = Vertex(min_x-dx*100,min_y-dy*100)
v2 = Vertex(min_x-dx*100,max_y+dy*200)
v3 = Vertex(max_x+dx*200,min_y-dy*100)

dt = Triangulation(v1,v2,v3,fast_locate=True)

for edge in dt.edges:
    edge.sym().rot().data = vertices
for vertex in vertices:
    vertex.containing_face = dt.initial_edge().sym()

for vertex in vertices:
    dt.insert_site(vertex)

#dt.remove_bounds()

root = tk.Tk()

def draw_faces():
    for face in dt.faces:
        if face.conflict:
            vis.add_drawable(Polygon2D(face.vertices(),fill="green"))
def draw_skeleton():
    for triangle in dt.get_triangles():
        prev = None
        for vertex in triangle:
            if prev:
                vis.add_drawable(Line2D(prev,vertex))
            vis.add_drawable(Point2D(vertex))
            prev = vertex 
        vis.add_drawable(Line2D(prev,triangle[0]))

def key_callback(event):
    dt.remove_bounds()
    draw_faces()
    draw_skeleton()
    vis.draw()

def mouse_callback(event):
    lock.acquire()

    vis.clear()
    v = Vertex(event.x,event.y)
    handle = dt.locate(v,safe=True,limit=100)
    if handle:
        vs = handle.face_vertices()
        vis.add_drawable(Polygon2D(vs,fill="red"))
        """
        for h in handle.neighbors():
            vs = h.face_vertices()
            vis.add_drawable(Polygon2D(vs,fill="blue"))
        """
    draw_skeleton()
    vis.draw()

    lock.release()

def click_callback(event):
    lock.acquire()

    v = Vertex(event.x,event.y)
    print v
    if dt.locate(v):
        dt.insert_site(v)
        vis.clear()
        draw_faces()
        draw_skeleton()
        vis.draw()

    lock.release()

vis = Visualizer(root,800,600,key_callback=key_callback,mouse_callback=mouse_callback,click_callback=click_callback)

draw_faces()
draw_skeleton()

vis.run()
root.mainloop()
