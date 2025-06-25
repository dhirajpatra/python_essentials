from collections import deque

class Graph:
    """
    A class to represent a graph using an adjacency list.
    The graph is unweighted and undirected for simplicity.
    """
    def __init__(self):
        """
        Initializes an empty graph.
        The adjacency list is a dictionary where keys are nodes
        and values are lists of connected nodes.
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

    def add_edge(self, node1, node2):
        """
        Adds an undirected edge between two nodes.
        If nodes do not exist, they are added first.
        """
        # Ensure both nodes exist in the graph
        self.add_node(node1)
        self.add_node(node2)

        # Add edge from node1 to node2 (if not already present)
        if node2 not in self.adj_list[node1]:
            self.adj_list[node1].append(node2)
            print(f"Edge added: {node1} -- {node2}")
        else:
            print(f"Edge {node1} -- {node2} already exists.")

        # Add edge from node2 to node1 (since it's undirected)
        if node1 not in self.adj_list[node2]:
            self.adj_list[node2].append(node1)
        # No else needed here as the print was already done for the first direction

    def get_nodes(self):
        """
        Returns a list of all nodes in the graph.
        """
        return list(self.adj_list.keys())

    def get_neighbors(self, node):
        """
        Returns a list of neighbors for a given node.
        """
        return self.adj_list.get(node, [])

    def display_graph(self):
        """
        Prints the adjacency list representation of the graph.
        """
        print("\nGraph Adjacency List:")
        for node, neighbors in self.adj_list.items():
            print(f"{node}: {neighbors}")

    def bfs(self, start_node):
        """
        Performs a Breadth-First Search (BFS) starting from a given node.
        BFS explores all the neighbor nodes at the present depth prior to moving on
        to nodes at the next depth level.

        Args:
            start_node: The node from which to start the BFS.

        Returns:
            A list of nodes in the order they were visited by BFS.
            Returns an empty list if the start_node is not in the graph.
        """
        if start_node not in self.adj_list:
            print(f"Start node '{start_node}' not found in the graph.")
            return []

        visited = set()         # To keep track of visited nodes
        queue = deque([start_node]) # Queue for BFS traversal
        bfs_order = []          # List to store the order of visited nodes

        visited.add(start_node) # Mark the start node as visited

        print(f"\nStarting BFS from node: '{start_node}'")
        while queue:
            current_node = queue.popleft() # Dequeue the front node
            bfs_order.append(current_node) # Add it to the traversal order
            print(f"Visiting node: {current_node}")

            # Explore neighbors of the current node
            for neighbor in self.adj_list[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)    # Mark neighbor as visited
                    queue.append(neighbor)   # Enqueue neighbor

        return bfs_order

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

    # Add edges
    my_graph.add_edge('A', 'B')
    my_graph.add_edge('A', 'C')
    my_graph.add_edge('B', 'D')
    my_graph.add_edge('C', 'E')
    my_graph.add_edge('D', 'F')
    my_graph.add_edge('E', 'F')
    my_graph.add_edge('A', 'D') # Add another edge to show different paths

    # Display the graph structure
    my_graph.display_graph()

    # Perform BFS traversal
    bfs_result = my_graph.bfs('A')
    print(f"\nBFS Traversal Order (starting from 'A'): {bfs_result}")

    bfs_result_c = my_graph.bfs('C')
    print(f"BFS Traversal Order (starting from 'C'): {bfs_result_c}")

    bfs_result_g = my_graph.bfs('G') # Test with a non-existent start node
    print(f"BFS Traversal Order (starting from 'G'): {bfs_result_g}")

    print("\nGraph and BFS program completed.")
