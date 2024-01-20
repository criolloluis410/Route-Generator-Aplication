class GraphK:
    def __init__(self, vertex):
        # Constructor that initializes the number of vertices and lists to store the graph and results
        self.V = vertex
        self.graph = []
        self.results = []

    def add_edge(self, u, v, w):
        # Method to add an edge to the graph with its respective vertices (u, v) and weight (w)
        self.graph.append([u, v, w])

    def search(self, parent, i):
        # Search function to find the set to which vertex 'i' belongs
        if parent[i] == i:
            return i
        return self.search(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        # Function to perform the union of two sets based on the set's height (rank)
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
        # Main method implementing the Kruskal's algorithm
        result = []  # List to store the resulting Minimum Spanning Tree
        i, e = 0, 0  # Counters for edges and vertices included in the Minimum Spanning Tree
        self.graph = sorted(self.graph, key=lambda item: item[2])  # Sorts edges by weight
        parent = []  # List to store the parents of the sets
        rank = []  # List to store the height of the sets (for union optimization)
        
        # Initialization of set parents and ranks for each vertex
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        
        # Iterates over all edges until V-1 edges are included in the Minimum Spanning Tree
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.search(parent, u)
            y = self.search(parent, v)
            
            # If including the edge does not form a cycle in the Minimum Spanning Tree, adds it
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        
        # Prints the edges of the Minimum Spanning Tree and stores the results in the 'results' list
        for u, v, weight in result:
            self.results.append((u, v, weight, '-'))
            print("Edge:", u, v, end=" ")
            print("-", weight)
