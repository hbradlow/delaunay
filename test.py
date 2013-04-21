from gui import Visualizer, Point2D, Line2D, Box2D, add_line
import Tkinter as tk
from structures import Vertex, QuadEdge, Edge, Face

vertices = [Vertex(250,100),Vertex(100,200),Vertex(200,300),Vertex(500,100)]
faces = [Face(),Face()]
edges = [Edge(vertices[0],vertices[1],left=faces[0]),Edge(vertices[1],vertices[2],right=faces[0]),Edge(vertices[0],vertices[2],left=faces[1],right=faces[1]),Edge(vertices[2],vertices[3],left=faces[1]),Edge(vertices[3],vertices[0],left=faces[1])]

vertices_to_add = [Vertex(200,150)]

root = tk.Tk()


vis = Visualizer(root,800,600)
for v in vertices:
    vis.add_drawable(Point2D(v))
for v in vertices_to_add:
    vis.add_drawable(Point2D(v,fill="green"))
for edge in edges:
    vis.add_drawable(Line2D(edge.origin,edge.desination))
vis.run()
root.mainloop()
