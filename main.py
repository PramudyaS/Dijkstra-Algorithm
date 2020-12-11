from collections import deque, namedtuple
from tkinter import *

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

def make_edge(start, end, cost=1):
  return Edge(start, end, cost)

class Graph:
    def __init__(self, edges):
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong Format Edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

    def  bind_path(self,path):
        label = str()
        Label(frm2,text="Shortest Result :",bg="white",font=('Arial Bold',18)).pack()
        for index,field in enumerate(path):
            if index == 0:
                label += field
            else:
                label += '-' + field

        Label(frm2, text=label, bg='white', font=('Arial',18)).pack()

#Define Graph Like Picture
graph = Graph([
    ("O", "A", 2),
    ("O", "B", 5),
    ("O", "C", 4),
    ("A", "F", 12),
    ("A", "D", 7),
    ("A", "B", 2),
    ("B", "D", 4),
    ("B", "E", 3),
    ("C", "B", 1),
    ("C", "E", 4),
    ("F", "T", 3),
    ("D", "T", 5),
    ("D", "E", 1),
    ("E", "T", 7)])

root = Tk()
root.title('Dijkstra Algorithm')

# frm = Frame(root, padx=20, height=150)
# Label(frm, text="Pramudya Saputra", font=("Arial Bold",12)).pack()
# Label(frm, text="41519110177", font=("Arial Bold",12)).pack()
#
# frm.pack(expand=FALSE, fill=NONE)


frm2 = LabelFrame(root, text='Shortest Path', bd=8, bg='white')
image = PhotoImage(file="general_path.png")
label = Label(frm2, image=image)
label.pack()

shorted_path = graph.dijkstra("O", "T")

path = graph.bind_path(shorted_path)

frm2.pack(expand=YES, fill=BOTH)

mainloop()