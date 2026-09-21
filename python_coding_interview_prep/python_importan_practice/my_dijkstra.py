import heapq
import sys

# Dijkstra's algorithm — used in Google Maps, GPS routing, network routing protocols.
# Time: O((V + E) log V) using min-heap | Space: O(V)

class Graph:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        # Adjacency list: {node: [(neighbor, weight), ...]}
        self.adj = {i: [] for i in range(num_vertices)}

    def add_edge(self, src: int, dest: int, weight: float):
        """Add a directed weighted edge."""
        self.adj[src].append((dest, weight))

    def dijkstra(self, source: int) -> list[float]:
        """
        Returns shortest distances from source to all vertices.
        Uses a min-heap for efficient next-node selection.
        """
        distances = [sys.maxsize] * self.num_vertices
        distances[source] = 0

        # Min-heap: (distance, vertex)
        heap = [(0, source)]

        while heap:
            curr_dist, curr_vertex = heapq.heappop(heap)

            # Skip if we already found a shorter path
            if curr_dist > distances[curr_vertex]:
                continue

            for neighbor, weight in self.adj[curr_vertex]:
                new_dist = curr_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor))

        return distances

    def print_shortest_paths(self, source: int):
        """Print shortest distances from source to all vertices."""
        distances = self.dijkstra(source)
        source_label = chr(ord('a') + source)
        for i, dist in enumerate(distances):
            print(f"Shortest distance from '{source_label}' to '{chr(ord('a') + i)}': {dist}")


if __name__ == "__main__":
    # Graph with 4 vertices (a=0, b=1, c=2, d=3)
    # Original adjacency matrix edges:
    # a->b: 3, a->c: 4, b->c: 0.5, c->d: 1
    g = Graph(num_vertices=4)
    g.add_edge(0, 1, 3)
    g.add_edge(0, 2, 4)
    g.add_edge(1, 2, 0.5)
    g.add_edge(2, 3, 1)

    g.print_shortest_paths(source=0)
