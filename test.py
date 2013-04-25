from gui import Visualizer, Point2D, Line2D, Box2D, add_line, Polygon2D
import Tkinter as tk
from structures import *
from dt import Triangulation

import IPython

#initial setup
vertices = [Vertex(550,100),Vertex(100,200),Vertex(500,500),Vertex(500,100)]

dt = Triangulation(vertices[0],vertices[1],vertices[2])

root = tk.Tk()

def draw_faces():
    for face in dt.faces:
        if face.conflict:
            vis.add_drawable(Polygon2D(face.vertices(),fill="green"))
def draw_skeleton():
    for edge in dt.initial_edge().q.all_edges():
        if edge.org() and edge.dest():
            vis.add_drawable(Line2D(edge.org(),edge.dest()))
            vis.add_drawable(Point2D(edge.org()))
            vis.add_drawable(Point2D(edge.dest()))

def key_callback(event):
    dt.insert_site(vertices_to_add.pop())
    draw_faces()
    draw_skeleton()
    vis.draw()

def mouse_callback(event):
    vis.clear()
    v = Vertex(event.x,event.y)
    handle = dt.locate(v)
    if handle:
        vs = handle.face_vertices()
        vis.add_drawable(Polygon2D(vs,fill="red"))
    draw_skeleton()
    vis.draw()

lock = False
def click_callback(event):
    global lock
    if lock:
        return
    lock = True
    v = Vertex(event.x,event.y)
    if dt.locate(v):
        for a in dt.insert_site(v):
            vis.clear()
            draw_faces()
            draw_skeleton()
            vis.draw()
    lock = False

vis = Visualizer(root,800,600,key_callback=key_callback,mouse_callback=mouse_callback,click_callback=click_callback)
draw_faces()
draw_skeleton()
vis.run()
root.mainloop()
