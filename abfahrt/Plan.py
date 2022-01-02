from typing import List
from typing import Tuple


class Plan:
    def __init__(self):
        self.nodes = []
        self.edges = [[]]
        self.distances = {}

    def add_node(self, node_id: int):
        self.nodes.append(node_id)

    def add_edge(self, from_node_id: int, to_node_id: int, length: int):
        if from_node_id <= len(self.edges)-1:
            self.edges[from_node_id].append(to_node_id)
            self.distances[(from_node_id, to_node_id)] = length
        else:
            for i in range(len(self.edges), from_node_id+1):
                self.edges.append([])
            self.edges[from_node_id].append(to_node_id)
            self.distances[(from_node_id, to_node_id)] = length

    def remove_edge(self, from_node_id: int, to_node_id: int):
        self.edges[from_node_id].remove(to_node_id)

    def dfs(self, v: int, visited: List[int]):
        visited[v] = True
        for u in self.edges[v]:
            if not visited[u]:
                self.dfs(u, visited)

    def is_connected(self) -> bool:
        visited = [True]
        for i in range(len(self.nodes)):
            visited.append(False)
        self.dfs(1, visited)
        t = 0
        for b in visited:
            if not b:
                return False
            t += 1
        return True

    def get_shortest_path(self, prev_list: List[int], target_id: int) -> List[int]:
        path = [target_id]
        self.shortest(target_id, prev_list, path)
        return path[::-1]

    def shortest(self, target_id: int, prev_list: List[int], path_to_target: List[int]):
        if prev_list[target_id]:
            path_to_target.append(prev_list[target_id])
            self.shortest(prev_list[target_id], prev_list, path_to_target)

    def dijkstra(self, start_id: int) -> Tuple[List[int], List[int]]:
        visited = [start_id]
        length_visited = [0]
        path = [0]

        for i in range(len(self.nodes)):
            length_visited.append(0)

        for i in range(len(self.nodes)):
            path.append(0)

        nodes = []

        for current_node in self.nodes:
            nodes.append(current_node)

        while len(nodes) > 0:
            min_node = None
            for node in nodes:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif length_visited[node] < length_visited[min_node]:
                        min_node = node
            if min_node is None:
                break

            nodes.remove(min_node)
            currentWeight = length_visited[min_node]

            for edge in self.edges[min_node]:
                length = currentWeight + self.distances[(min_node, edge)]
                if edge not in visited or (length < length_visited[edge] and edge in visited):
                    length_visited[edge] = length
                    visited.append(edge)
                    path[edge] = min_node

        return visited, path
