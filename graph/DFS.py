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

            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    _dfs_recursive(neighbor)

        _dfs_recursive(start_node)
        return dfs_order

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
    my_graph.add_node('G') # Add one more node for a slightly larger graph

    # Add edges to create a sample graph
    my_graph.add_edge('A', 'B')
    my_graph.add_edge('A', 'C')
    my_graph.add_edge('B', 'D')
    my_graph.add_edge('B', 'E')
    my_graph.add_edge('C', 'F')
    my_graph.add_edge('D', 'G')
    my_graph.add_edge('E', 'G') # Create a path from E to G
    my_graph.add_edge('F', 'G') # Create a path from F to G

    # Display the graph structure
    my_graph.display_graph()

    # Perform DFS traversal
    dfs_result_a = my_graph.dfs('A')
    print(f"\nDFS Traversal Order (starting from 'A'): {dfs_result_a}")

    dfs_result_c = my_graph.dfs('C')
    print(f"\nDFS Traversal Order (starting from 'C'): {dfs_result_c}")

    dfs_result_x = my_graph.dfs('X') # Test with a non-existent start node
    print(f"\nDFS Traversal Order (starting from 'X'): {dfs_result_x}")

    print("\nGraph and DFS program completed.")
