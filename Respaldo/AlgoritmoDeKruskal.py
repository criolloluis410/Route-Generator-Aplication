class GraphK:
    def __init__(self, vertex):
        self.V = vertex
        self.graph = []
        self.resultados = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def search(self, parent, i):
        if parent[i] == i:
            return i
        return self.search(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.search(parent, x)
        yroot = self.search(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.search(parent, u)
            y = self.search(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        for u, v, weight in result:
            self.resultados.append((u, v, weight, '-'))
            print("Edge:", u, v, end=" ")
            print("-", weight)

'''
g = Graph(5)
g.add_edge(0, 1, 8)
g.add_edge(0, 2, 5)
g.add_edge(1, 2, 9)
g.add_edge(1, 3, 11)
g.add_edge(2, 3, 15)
g.add_edge(2, 4, 10)
g.add_edge(3, 4, 7)
g.kruskal()
listaDePrueba=[(0, 1, 8),(0, 2, 5),(1, 2, 9),(1, 3, 11),(2, 3, 15),(2, 4, 10),(3, 4, 7)]
g2= Graph(5)
for dat in listaDePrueba:
    print(dat)
    g2.add_edge(dat[0],dat[1],dat[2 ])
g2.kruskal()
print(listaDePrueba)
#

g = GraphK(3)
g.add_edge(0, 1, 4)
g.add_edge(0, 2, 5)
g.add_edge(1, 0, 3)
g.add_edge(1, 2, 10)
g.add_edge(2, 0, 5)
g.add_edge(2, 1, 11)
g.kruskal()
'''
'''
g = GraphK(4)
g.add_edge(0, 2, 4)
g.add_edge(1, 0, 7)
g.add_edge(2, 0, 5)
g.add_edge(3, 0, 6)
g.add_edge(2, 1, 8)
g.add_edge(3, 1, 5)
g.add_edge(1, 2, 6)
g.add_edge(3, 2, 9)
g.add_edge(1, 3, 5)
g.add_edge(2, 3, 6)

g.kruskal()
print(g.resultados)

nodosDstNuev=[]
nodoGW=0

for i,ruta in enumerate(g.resultados):
#for i, obj in enumerate(g.resultados):
    if  ruta[0]==nodoGW:
        g.resultados[i] = (ruta[1],ruta[0],ruta[2],'m')# se deberia modificar el peso
        print('mg')
        print( g.resultados[i])
        #nodosDstNuev.append(ruta[0])
print(g.resultados)
print(nodosDstNuev)

for i,ruta in enumerate(g.resultados):
#for i, obj in enumerate(g.resultados):
    if  ruta[1]==nodoGW:
        g.resultados[i] = (ruta[0],ruta[1],ruta[2],'v')
        print( g.resultados[i])
        nodosDstNuev.append(ruta[0])
print(g.resultados)
print(nodosDstNuev)

for i,ruta in enumerate(g.resultados):
#for i, obj in enumerate(g.resultados):
    if  ruta[3]!='v':
        print( g.resultados[i])
        for dst in nodosDstNuev:
            if ruta[1]==dst:
                g.resultados[i] = (ruta[0],ruta[1],ruta[2],'v')
                nodosDstNuev.append(ruta[0])

print(g.resultados)
print(nodosDstNuev)

for i,ruta in enumerate(g.resultados):
#for i, obj in enumerate(g.resultados):
    if  ruta[3]!='v':
        print( g.resultados[i])
        for rtc in g.resultados:
            if ruta[0]==rtc[0] and rtc[3]=='v' :
                g.resultados[i] = (ruta[1],ruta[0],ruta[2],'v')
                nodosDstNuev.append(ruta[1])
print(g.resultados)
print(nodosDstNuev)
'''
'''
g2 = GraphK(3)
g2.add_edge(0, 2, 4)
g2.add_edge(2, 0, 11)
g2.add_edge(1, 2, 11)

g2.kruskal()
'''