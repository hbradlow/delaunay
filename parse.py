from structures import *
def output_ele(filename,triangles):
    with open(filename,"w") as f:
        s = str(len(triangles)) + " 3 " + "0\n"
        f.write(s)
        for index,t in enumerate(triangles):
            s = str(index) + " " + str(t[0].index) + " " + str(t[1].index) + " " + str(t[2].index) + "\n"
            f.write(s)

def load_node(filename):
    vertices = []
    with open(filename,"r") as f:
        l = [a.strip() for a in f.readline().split(" ") if a]
        num_vertices = int(l[0])
        for i in range(num_vertices):
            l = [a.strip() for a in f.readline().split(" ") if a]
            x = 300+50*float(l[1])
            y = 300+50*float(l[2])
            vertices.append(Vertex(x,y,index=int(l[0])))
    return vertices

def write_node(filename,vertices):
    with open(filename,"w") as f:
        s = str(len(vertices)) + " 2 0 0\n"
        f.write(s)
        for index,v in enumerate(vertices):
            f.write(str(index) + " " + str(v.x) + " " + str(v.y) + "\n")

def generate_grid(size=10):
    vertices = []
    for i in range(size):
        for j in range(size):
            vertices.append(Vertex(i,j))
    return vertices

if __name__=="__main__":
    print load_node("spiral.node")
