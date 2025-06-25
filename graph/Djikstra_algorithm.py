import heapq # For Dijkstra's priority queue
from collections import deque

class Graph:
    """
    A class to represent a graph using an adjacency list.
    The graph can be unweighted (default weight 1) or weighted.
    It is undirected for simplicity.
    """
    def __init__(self):
        """
        Initializes an empty graph.
        The adjacency list is a dictionary where keys are nodes
        and values are lists of tuples (neighbor, weight).
        For unweighted graphs, the weight defaults to 1.
        """
        self.adj_list = {}

    def add_node(self, node):
        """
        Adds a new node to the graph if it doesn't already exist.
        """
        if node not in self.adj_list:
            self.adj_list[node] = []
            print(f"Node '{node}' added.")
        else:
            print(f"Node '{node}' already exists.")

    def add_edge(self, node1, node2, weight=1):
        """
        Adds an undirected edge between two nodes with an optional weight.
        If nodes do not exist, they are added first.

        Args:
            node1: The first node.
            node2: The second node.
            weight: The weight of the edge (default is 1 for unweighted).
        """
        # Ensure both nodes exist in the graph
        self.add_node(node1)
        self.add_node(node2)

        # Add edge from node1 to node2 (if not already present with this weight)
        edge1_exists = False
        for i, (neighbor, existing_weight) in enumerate(self.adj_list[node1]):
            if neighbor == node2:
                if existing_weight != weight:
                    self.adj_list[node1][i] = (node2, weight) # Update weight if different
                    print(f"Updated edge {node1} -- {node2} to weight {weight}.")
                else:
                    print(f"Edge {node1} -- {node2} with weight {weight} already exists.")
                edge1_exists = True
                break
        if not edge1_exists:
            self.adj_list[node1].append((node2, weight))
            print(f"Edge added: {node1} -- {node2} (Weight: {weight})")

        # Add edge from node2 to node1 (since it's undirected)
        edge2_exists = False
        for i, (neighbor, existing_weight) in enumerate(self.adj_list[node2]):
            if neighbor == node1:
                if existing_weight != weight:
                    self.adj_list[node2][i] = (node1, weight) # Update weight if different
                edge2_exists = True
                break
        if not edge2_exists:
            self.adj_list[node2].append((node1, weight))


    def get_nodes(self):
        """
        Returns a list of all nodes in the graph.
        """
        return list(self.adj_list.keys())

    def get_neighbors(self, node):
        """
        Returns a list of neighbors (without weights) for a given node.
        """
        return [neighbor for neighbor, _ in self.adj_list.get(node, [])]

    def display_graph(self):
        """
        Prints the adjacency list representation of the graph, including weights.
        """
        print("\nGraph Adjacency List (Node: [(Neighbor, Weight), ...]):")
        for node, neighbors_with_weights in self.adj_list.items():
            # Format output nicely for display
            formatted_neighbors = ", ".join([f"({n}, {w})" for n, w in neighbors_with_weights])
            print(f"{node}: [{formatted_neighbors}]")

    def dfs(self, start_node):
        """
        Performs a Depth-First Search (DFS) starting from a given node.
        DFS explores as far as possible along each branch before backtracking.

        Args:
            start_node: The node from which to start the DFS.

        Returns:
            A list of nodes in the order they were visited by DFS.
            Returns an empty list if the start_node is not in the graph.
        """
        if start_node not in self.adj_list:
            print(f"Start node '{start_node}' not found in the graph.")
            return []

        visited = set()     # To keep track of visited nodes
        dfs_order = []      # List to store the order of visited nodes

        print(f"\nStarting DFS from node: '{start_node}'")

        def _dfs_recursive(node):
            """
            Helper function for recursive DFS.
            """
            visited.add(node)
            dfs_order.append(node)
            print(f"Visiting node: {node}")

            # Iterate over neighbors, ignoring weights for DFS traversal
            for neighbor, _ in self.adj_list[node]:
                if neighbor not in visited:
                    _dfs_recursive(neighbor)

        _dfs_recursive(start_node)
        return dfs_order

    def dijkstra(self, start_node):
        """
        Performs Dijkstra's algorithm to find the shortest paths from a
        start_node to all other nodes in the graph.

        Args:
            start_node: The node from which to start finding shortest paths.

        Returns:
            A tuple containing:
            - distances: A dictionary with the shortest distance from start_node to each node.
                         Nodes unreachable will have a distance of float('inf').
            - predecessors: A dictionary mapping each node to its predecessor in the
                            shortest path from the start_node.
            Returns empty dictionaries if the start_node is not in the graph.
        """
        if start_node not in self.adj_list:
            print(f"Start node '{start_node}' not found in the graph for Dijkstra.")
            return {}, {}

        # Initialize distances: all to infinity, start_node to 0
        distances = {node: float('inf') for node in self.adj_list}
        distances[start_node] = 0

        # Priority queue: stores tuples of (distance, node)
        # heapq is a min-heap, so it will always pop the smallest distance first
        priority_queue = [(0, start_node)] # (distance, node)

        # Predecessors: to reconstruct the shortest path
        predecessors = {node: None for node in self.adj_list}

        print(f"\nStarting Dijkstra's algorithm from node: '{start_node}'")

        while priority_queue:
            # Get the node with the smallest distance from the priority queue
            current_distance, current_node = heapq.heappop(priority_queue)

            # If we've already found a shorter path to this node, skip
            if current_distance > distances[current_node]:
                continue

            print(f"Processing node: {current_node} (Current shortest distance: {current_distance})")

            # Explore neighbors
            for neighbor, weight in self.adj_list[current_node]:
                distance = current_distance + weight

                # If a shorter path to the neighbor is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
                    print(f"  Updated path to {neighbor}: New distance {distance} via {current_node}")

        return distances, predecessors

# --- Example Usage ---
if __name__ == "__main__":
    # Create a new graph instance
    my_graph = Graph()

    # Add nodes
    my_graph.add_node('A')
    my_graph.add_node('B')
    my_graph.add_node('C')
    my_graph.add_node('D')
    my_graph.add_node('E')
    my_graph.add_node('F')
    my_graph.add_node('G')

    # Add edges for a sample graph with weights
    print("\nAdding edges with weights for Dijkstra's demonstration:")
    my_graph.add_edge('A', 'B', 4)
    my_graph.add_edge('A', 'C', 2)
    my_graph.add_edge('B', 'E', 3)
    my_graph.add_edge('C', 'D', 2)
    my_graph.add_edge('C', 'F', 4)
    my_graph.add_edge('D', 'E', 3)
    my_graph.add_edge('D', 'F', 1)
    my_graph.add_edge('E', 'G', 2)
    my_graph.add_edge('F', 'G', 3)
    my_graph.add_edge('B', 'D', 5) # Another edge for complexity

    # Display the graph structure
    my_graph.display_graph()

    # --- DFS Traversal (unaffected by weights in its logic, but adj_list now has weights) ---
    dfs_result_a = my_graph.dfs('A')
    print(f"\nDFS Traversal Order (starting from 'A'): {dfs_result_a}")

    # --- Dijkstra's Algorithm ---
    print("\n--- Running Dijkstra's Algorithm ---")
    distances, predecessors = my_graph.dijkstra('A')

    print("\nShortest Distances from 'A':")
    for node, dist in distances.items():
        print(f"  To {node}: {dist if dist != float('inf') else 'Unreachable'}")

    print("\nPredecessors for Shortest Paths from 'A':")
    for node, pred in predecessors.items():
        print(f"  {node}: {pred}")

    # Example: Reconstruct path to 'G'
    print("\nReconstructing Shortest Path to 'G' from 'A':")
    path = []
    current = 'G'
    if distances['G'] == float('inf'):
        print("  'G' is unreachable from 'A'.")
    else:
        while current is not None:
            path.insert(0, current)
            current = predecessors[current]
        print(f"  Path: {' -> '.join(path)}")
        print(f"  Total Distance: {distances['G']}")

    # Test Dijkstra with a non-existent start node
    distances_x, predecessors_x = my_graph.dijkstra('X')
    print(f"\nDistances from 'X': {distances_x}")
    print(f"Predecessors from 'X': {predecessors_x}")

    print("\nGraph, DFS, and Dijkstra's programs completed.")
