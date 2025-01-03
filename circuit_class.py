class Circuit:
    def __init__(self, file_path):
        """
        Initializes a Circuit object by reading from the specified file.

        Args:
            file_path (str): Path to the text file containing the circuit description.
        """
        self.file_path = file_path
        self.nodes = {}
        self.inputs = []
        self.outputs = []
        self.component_delays = {
            "ADD": 1.0,
            "MUL": 1.0,
            "REG": 0.2,
            "MUX": 1.0,
            "DEFAULT": 0.5,
        }
        self.read_circuit()

    def read_circuit(self):
        """
        Reads a circuit description from a text file and populates the nodes.
        """
        node_counter = 0

        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split()
                    if len(parts) < 2:
                        raise ValueError(f"Invalid line format: {line}")

                    node_type, node_id = parts[0], parts[1]
                    inputs = parts[2:] if len(parts) > 2 else []

                    # Assign a unique ID to the node
                    unique_id = f"node_{node_counter}"
                    node_counter += 1

                    # Store the node details
                    self.nodes[node_id] = {
                        "unique_id": unique_id,
                        "type": node_type,
                        "inputs": inputs,
                        "outputs": [],
                    }

                    if node_type == "INPUT":
                        self.inputs.append(node_id)
                    elif node_type == "OUTPUT":
                        self.outputs.append(node_id)

            # Populate outputs for each node
            for node_id, details in self.nodes.items():
                for input_id in details["inputs"]:
                    if input_id not in self.nodes:
                        raise ValueError(f"Undefined input node: {input_id}")
                    self.nodes[input_id]["outputs"].append(node_id)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except ValueError as ve:
            raise ValueError(f"Error reading circuit: {ve}")

    def find_critical_path(self):
        """
        Finds the critical path in the circuit.

        Returns:
            tuple: Critical path as a sequence of node IDs, total delay, and components with their delays.
        """
        delays = {}
        predecessors = {}

        # Initialize delays for input nodes
        for node_id in self.inputs:
            delays[node_id] = 0

        # Topologically sort the nodes
        sorted_nodes = self.topological_sort()

        # Calculate delays and predecessors
        for node_id in sorted_nodes:
            node = self.nodes[node_id]
            node_type = node["type"]
            max_input_delay = 0
            for input_id in node["inputs"]:
                max_input_delay = max(max_input_delay, delays[input_id])

            component_delay = self.component_delays.get(node_type, self.component_delays["DEFAULT"])
            delays[node_id] = max_input_delay + component_delay

            for input_id in node["inputs"]:
                if delays[node_id] == delays[input_id] + component_delay:
                    predecessors[node_id] = input_id

        # Find the output node with the maximum delay
        critical_output = max(self.outputs, key=lambda node_id: delays[node_id])
        total_delay = delays[critical_output]

        # Reconstruct the critical path
        critical_path = []
        current_node = critical_output
        while current_node in predecessors:
            critical_path.insert(0, current_node)
            current_node = predecessors[current_node]
        critical_path.insert(0, current_node)

        components_with_delays = [
            (node_id, self.component_delays.get(self.nodes[node_id]["type"], self.component_delays["DEFAULT"]))
            for node_id in critical_path
        ]

        return critical_path, total_delay, components_with_delays

    def topological_sort(self):
        """
        Performs a topological sort of the circuit nodes.

        Returns:
            list: A list of node IDs in topological order.
        """
        in_degree = {node_id: 0 for node_id in self.nodes}
        for node_id, details in self.nodes.items():
            for input_id in details["inputs"]:
                in_degree[node_id] += 1

        queue = [node for node in in_degree if in_degree[node] == 0]
        sorted_nodes = []

        while queue:
            current = queue.pop(0)
            sorted_nodes.append(current)

            for neighbor in self.nodes[current]["outputs"]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return sorted_nodes
