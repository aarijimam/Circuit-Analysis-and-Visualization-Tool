from graphviz import Digraph

def visualize_circuit(circuit, output_file="circuit"):
    """
    Visualizes the circuit as a directed graph.
    
    Args:
        circuit (dict): The circuit structure containing nodes and their details.
        output_file (str): The name of the output file (without extension) for the visualization.
    """
    try:
        graph = Digraph(format="png")
        graph.attr(rankdir="LR")  # Layout from left to right

        # Add nodes to the graph
        for node_id, details in circuit["nodes"].items():
            label = f"{node_id}\\n{details['type']}"
            shape = "ellipse" if details["type"] in ["INPUT", "OUTPUT"] else "box"
            graph.node(details["unique_id"], label=label, shape=shape)
        
        # Add edges to the graph
        for node_id, details in circuit["nodes"].items():
            for input_id in details["inputs"]:
                graph.edge(circuit["nodes"][input_id]["unique_id"], details["unique_id"])

        # Render the graph
        graph.render(output_file, cleanup=True)
        print(f"Circuit visualization saved to {output_file}.png")
    except Exception as e:
        print(f"Error visualizing the circuit: {e}")

def visualize_circuit_with_critical_path(circuit, critical_path, output_file="circuit_with_critical_path"):
    """
    Visualizes the circuit and highlights the critical path.

    Args:
        circuit (dict): The circuit structure containing nodes and their details.
        critical_path (list): List of node IDs in the critical path.
        output_file (str): The name of the output file (without extension) for the visualization.
    """
    try:
        graph = Digraph(format="png")
        graph.attr(rankdir="LR")  # Layout from left to right

        # Set of edges in the critical path
        critical_edges = set(
            (critical_path[i], critical_path[i + 1]) for i in range(len(critical_path) - 1)
        )

        # Add nodes to the graph
        for node_id, details in circuit["nodes"].items():
            label = f"{node_id}\\n{details['type']}"
            shape = "ellipse" if details["type"] in ["INPUT", "OUTPUT"] else "box"
            color = "red" if node_id in critical_path else "black"
            graph.node(details["unique_id"], label=label, shape=shape, color=color)

        # Add edges to the graph
        for node_id, details in circuit["nodes"].items():
            for input_id in details["inputs"]:
                edge_color = "red" if (input_id, node_id) in critical_edges else "black"
                graph.edge(circuit["nodes"][input_id]["unique_id"], details["unique_id"], color=edge_color)

        # Render the graph
        graph.render(output_file, cleanup=True)
        print(f"Circuit visualization with critical path saved to {output_file}.png")
    except KeyError as e:
        print(f"Missing key in the circuit structure: {e}")
    except Exception as e:
        print(f"Error visualizing the circuit with critical path: {e}")

def read_circuit(file_path):
    """
    Reads a circuit description from a text file and stores the data in a suitable structure.
    
    Args:
        file_path (str): Path to the text file containing the circuit description.
        
    Returns:
        dict: A dictionary with the circuit structure, including nodes and their properties.
    """
    try:
        circuit = {
            "nodes": {},  # Dictionary to store nodes and their details
            "inputs": [],  # List of input node IDs
            "outputs": []  # List of output node IDs
        }

        node_counter = 0  # Counter to assign unique IDs to nodes

        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # Skip comments and empty lines

                parts = line.split()
                if len(parts) < 2:
                    raise ValueError(f"Invalid line format: {line}")

                node_type, node_id = parts[0], parts[1]
                inputs = parts[2:] if len(parts) > 2 else []

                # Assign a unique ID to the node
                unique_id = f"node_{node_counter}"
                node_counter += 1

                # Store the node details in the dictionary
                circuit["nodes"][node_id] = {
                    "unique_id": unique_id,
                    "type": node_type,
                    "inputs": inputs,
                    "outputs": []  # Outputs will be populated later
                }

                # Identify input and output nodes
                if node_type == "INPUT":
                    circuit["inputs"].append(node_id)
                elif node_type == "OUTPUT":
                    circuit["outputs"].append(node_id)

        # Populate outputs for each node
        for node_id, details in circuit["nodes"].items():
            for input_id in details["inputs"]:
                if input_id not in circuit["nodes"]:
                    raise KeyError(f"Input {input_id} referenced by {node_id} not found in nodes.")
                circuit["nodes"][input_id]["outputs"].append(node_id)

        return circuit
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading the circuit file: {e}")
        return None

def find_critical_path(circuit):
    """
    Finds the critical path and total delay of the circuit.

    Args:
        circuit (dict): The circuit structure containing nodes and their details.

    Returns:
        tuple: Critical path as a sequence of node IDs, total delay, and components with their delays.
    """
    try:
        delays = {}  # Store the delay to reach each node
        predecessors = {}  # Store the predecessor of each node in the critical path

        # Initialize delays for input nodes to 0
        for node_id in circuit["inputs"]:
            delays[node_id] = 0

        # Topologically sort the nodes
        sorted_nodes = []
        in_degree = {node_id: 0 for node_id in circuit["nodes"]}

        for node_id, details in circuit["nodes"].items():
            for input_id in details["inputs"]:
                in_degree[node_id] += 1

        queue = [node for node in in_degree if in_degree[node] == 0]

        while queue:
            current = queue.pop(0)
            sorted_nodes.append(current)

            for neighbor in circuit["nodes"][current]["outputs"]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Calculate delays and critical path
        for node_id in sorted_nodes:
            node = circuit["nodes"][node_id]
            node_type = node["type"]
            max_input_delay = 0
            for input_id in node["inputs"]:
                if input_id in delays:
                    max_input_delay = max(max_input_delay, delays[input_id])

            component_delay = component_delays.get(node_type, component_delays["DEFAULT"])
            delays[node_id] = max_input_delay + component_delay

            for input_id in node["inputs"]:
                if delays[node_id] == delays[input_id] + component_delay:
                    predecessors[node_id] = input_id

        # Find the output node with the maximum delay
        critical_output = max(circuit["outputs"], key=lambda node_id: delays[node_id])
        total_delay = delays[critical_output]

        # Reconstruct the critical path
        critical_path = []
        current_node = critical_output
        while current_node in predecessors:
            critical_path.insert(0, current_node)
            current_node = predecessors[current_node]
        critical_path.insert(0, current_node)

        # Get components and their delays in the critical path
        components_with_delays = [
            (node_id, component_delays.get(circuit["nodes"][node_id]["type"], component_delays["DEFAULT"]))
            for node_id in critical_path
        ]

        return critical_path, total_delay, components_with_delays
    except Exception as e:
        print(f"Error finding the critical path: {e}")
        return [], 0, []

# Dictionary to store component delays
component_delays = {
    "ADD": 1.0,        # Adder delay
    "MUL": 1.0,        # Multiplier delay
    "REG": 0.2,        # Register delay
    "MUX": 1.0,        # Multiplexor delay
    "DEFAULT": 0.5     # Default delay for other structures
}

# Example usage
def main():
    circuits = ["circuit1", "circuit2", "circuit3", "circuit_error"]
    for cir_name in circuits:
        circuit_graph = read_circuit(f"{cir_name}.txt")
        if circuit_graph is None:
            continue
        
        critical_path, total_delay, components_with_delays = find_critical_path(circuit_graph)
        
        print(f"Critical Path: {' -> '.join(critical_path)}")
        print(f"Total Delay: {total_delay:.2f} time units")
        print("Components in Critical Path with Delays:")
        for component, delay in components_with_delays:
            print(f"  {component}: {delay:.2f} time units")
            
        visualize_circuit_with_critical_path(circuit_graph, critical_path, output_file=f"{cir_name}_visualization")

if __name__ == "__main__":
    main()
