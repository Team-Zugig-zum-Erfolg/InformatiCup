class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = [[]]
        self.distances = {}
    
    def addNode(self,value):
        self.nodes.append(value)
    
    def addEdge(self, fromNode, toNode, distance):
        if fromNode <= len(self.edges)-1:
            self.edges[fromNode].append(toNode)
            self.distances[(fromNode, toNode)] = distance
        else:
            for i in range(len(self.edges),fromNode+1):
                self.edges.append([])
            self.edges[fromNode].append(toNode)
            self.distances[(fromNode, toNode)] = distance
            
    def removeEdge(self, fromNode, toNode):
        self.edges[fromNode].remove(toNode)
        

def shortest(v, path, path_to_target):
    ''' make shortest path from v.previous'''
    #print(path[v])
    if path[v]:
        path_to_target.append(path[v])
        shortest(path[v], path, path_to_target)
    return



def dijkstra(graph, initial):
    visited = [initial]
    weight_visited = [0]
    path = [0]

    for i in range(len(graph.nodes)):
        weight_visited.append(0)

    for i in range(len(graph.nodes)):
        path.append(0)

    nodes = graph.nodes



    while len(nodes)>0:
        minNode = None
        for node in nodes:
            if node in visited:
                if minNode is None:
                    minNode = node
                elif weight_visited[node] < weight_visited[minNode]:
                    minNode = node
        if minNode is None:
            break



        nodes.remove(minNode)
        currentWeight = weight_visited[minNode]

        for edge in graph.edges[minNode]:
            weight = currentWeight + graph.distances[(minNode, edge)]
            if edge not in visited or (weight < weight_visited[edge] and edge in visited):
                weight_visited[edge] = weight
                visited.append(edge)
                path[edge] = minNode
           
    return visited, path

customGraph = Graph()

for i in range(200):
    customGraph.addNode(i)


for i in range(200):
    for t in range(1,200):
        if i != t:
            customGraph.addEdge(i, t, 2)
          

#example
customGraph.removeEdge(1,10)
customGraph.removeEdge(1,2)
customGraph.removeEdge(10,2)


out, path_out = dijkstra(customGraph,1)

path = [2]
shortest(2, path_out, path)
print('The shortest path : %s' %(path[::-1]))
