from structures import *
from dt import Triangulation
from parse import load_node, output_ele
import sys
import time

start_time = time.time()

filename = "spiral.node"
if len(sys.argv)>1:
    filename = sys.argv[1]

basename = ".".join(filename.split(".")[:-1])


#initial setup
vertices = load_node(filename)
min_x = min(vertices,key=lambda v: v.x).x
min_y = min(vertices,key=lambda v: v.y).y
max_x = max(vertices,key=lambda v: v.x).x
max_y = max(vertices,key=lambda v: v.y).y

dx = max_x-min_x
dy = max_y-min_y

v1 = Vertex(min_x-dx*100,min_y-dy*100)
v2 = Vertex(min_x-dx*100,max_y+dy*200)
v3 = Vertex(max_x+dx*200,min_y-dy*100)

dt = Triangulation(v1,v2,v3)

total = len(vertices)
for index,vertex in enumerate(vertices):
    if index%100==0:
        print 100.*index/total,"percent complete"
    dt.insert_site(vertex)

dt.remove_bounds()
output_ele(basename + ".ele",dt.get_triangles())

print "Took",time.time()-start_time,"seconds to complete"
