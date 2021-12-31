class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = [[]]
        self.distances = {}

    def addNode(self, value):
        self.nodes.append(value)

    def addEdge(self, fromNode, toNode, distance):
        if fromNode <= len(self.edges)-1:
            self.edges[fromNode].append(toNode)
            self.distances[(fromNode, toNode)] = distance
        else:
            for i in range(len(self.edges), fromNode+1):
                self.edges.append([])
            self.edges[fromNode].append(toNode)
            self.distances[(fromNode, toNode)] = distance

    def removeEdge(self, fromNode, toNode):
        self.edges[fromNode].remove(toNode)

    @staticmethod
    def dfs(graph, v, visited):
        visited[v] = True
        for u in graph.edges[v]:
            if not visited[u]:
                Graph.dfs(graph, u, visited)

    @staticmethod
    def is_connected(graph):
        visited = [True]
        for i in range(len(graph.nodes)):
            visited.append(False)
        Graph.dfs(graph, 1, visited)
        t = 0
        for b in visited:
            if not b:
                return False
            t += 1
        return True

    @staticmethod
    def shortest(v, prev_list, path_to_target):
        if prev_list[v]:
            path_to_target.append(prev_list[v])
            Graph.shortest(prev_list[v], prev_list, path_to_target)
        return

    @staticmethod
    def dijkstra(graph, initial):
        visited = [initial]
        weight_visited = [0]
        path = [0]

        for i in range(len(graph.nodes)):
            weight_visited.append(0)

        for i in range(len(graph.nodes)):
            path.append(0)

        nodes = []

        for current_node in graph.nodes:
            nodes.append(current_node)

        while len(nodes) > 0:
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
