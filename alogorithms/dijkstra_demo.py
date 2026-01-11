import heapq
import sys


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def add_edge(self, src, dest, weight):
        """Add an edge to the graph"""
        self.graph[src][dest] = weight
        self.graph[dest][src] = weight  # For undirected graph

    def print_solution(self, dist, prev):
        """Print the solution"""
        print("Vertex \t Distance from Source \t Path")
        for node in range(self.V):
            # Reconstruct path
            path = []
            # Backtrack from the node to the source using prev array
            current = node

            # Build the path in reverse order
            while current is not None:
                # Insert at the beginning to reverse the path
                path.insert(0, current)
                # Move to the previous node
                current = prev[current]

            print(f"{node} \t\t {dist[node]} \t\t\t {path}")

    def dijkstra(self, src):
        """Dijkstra's algorithm implementation"""
        # Initialize distances: set all distances to infinity
        dist = [float('inf')] * self.V
        # Distance from source to itself is 0
        dist[src] = 0

        # Priority queue (min-heap) to store vertices to process
        # Format: (distance, vertex)
        pq = []
        heapq.heappush(pq, (0, src))

        # Previous nodes to reconstruct paths
        prev = [None] * self.V

        # Keep track of visited vertices
        visited = [False] * self.V

        print(f"Starting Dijkstra's algorithm from source vertex {src}")
        print("=" * 60)

        step = 1
        while pq:
            print(f"\nStep {step}:")
            print("Priority queue (distance, vertex):", pq)

            # Extract the vertex with minimum distance
            current_dist, u = heapq.heappop(pq)

            # Skip if we've already processed this vertex with a shorter distance
            if visited[u]:
                print(f"  Vertex {u} already visited, skipping...")
                continue

            print(f"  Processing vertex {u} with current distance {current_dist}")

            # Mark the vertex as visited
            visited[u] = True

            # Update distances of adjacent vertices
            for v in range(self.V):
                # Check if there's an edge from u to v
                if self.graph[u][v] > 0:
                    print(f"    Checking neighbor {v} (edge weight: {self.graph[u][v]})")

                    # Calculate new distance through u
                    new_dist = dist[u] + self.graph[u][v]

                    # If we found a shorter path to v
                    if not visited[v] and new_dist < dist[v]:
                        print(f"      Found shorter path to {v}: {new_dist} (was {dist[v]})")
                        dist[v] = new_dist
                        prev[v] = u
                        heapq.heappush(pq, (new_dist, v))
                    else:
                        print(f"      No improvement (current best: {dist[v]})")

            step += 1

        print("\n" + "=" * 60)
        print("Algorithm completed!")
        print(f"\nFinal distances from source vertex {src}:")
        self.print_solution(dist, prev)

        return dist, prev


def main():
    """Main function to demonstrate Dijkstra's algorithm"""
    print("=" * 60)
    print("DIJKSTRA'S ALGORITHM VISUALIZATION")
    print("=" * 60)

    # Create a sample graph
    # Let's create a graph with 6 vertices (0 to 5)
    g = Graph(6)

    # Add edges with weights
    g.add_edge(0, 1, 7)
    g.add_edge(0, 2, 9)
    g.add_edge(0, 5, 14)
    g.add_edge(1, 2, 10)
    g.add_edge(1, 3, 15)
    g.add_edge(2, 3, 11)
    g.add_edge(2, 5, 2)
    g.add_edge(3, 4, 6)
    g.add_edge(4, 5, 9)

    print("\nGraph representation (adjacency matrix):")
    for row in g.graph:
        print(row)

    print("\n" + "=" * 60)
    print("Visual representation of the graph:")
    print("""
          (0)
       7/  | \\14
      (1) 9|  (5)
    10/  \\ |  /9
    (2)-11-(3) |
        15\\ | /6
           (4)
    """)

    # Run Dijkstra's algorithm from source vertex 0
    source = 0
    distances, predecessors = g.dijkstra(source)

    # Show an example path reconstruction
    print("\n" + "=" * 60)
    target = 4
    print(f"Example: Path from source {source} to target {target}:")

    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]

    print(f"Path: {' -> '.join(map(str, path))}")
    print(f"Total distance: {distances[target]}")


if __name__ == "__main__":
    main()