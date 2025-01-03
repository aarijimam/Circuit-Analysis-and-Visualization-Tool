from graphviz import Digraph

class CircuitVisualizer:
    @staticmethod
    def visualize_circuit(circuit, output_file="circuit"):
        """
        Visualizes the circuit as a directed graph.

        Args:
            circuit (Circuit): The Circuit object.
            output_file (str): The name of the output file (without extension).
        """
        graph = Digraph(format="png")
        graph.attr(rankdir="LR")

        for node_id, details in circuit.nodes.items():
            label = f"{node_id}\\n{details['type']}"
            shape = "ellipse" if details["type"] in ["INPUT", "OUTPUT"] else "box"
            graph.node(details["unique_id"], label=label, shape=shape)

        for node_id, details in circuit.nodes.items():
            for input_id in details["inputs"]:
                graph.edge(circuit.nodes[input_id]["unique_id"], details["unique_id"])

        graph.render(f"./outputs/{output_file}", cleanup=True)
        print(f"Circuit visualization saved to {output_file}.png")

    @staticmethod
    def visualize_with_critical_path(circuit, critical_path, output_file="circuit_with_critical_path"):
        """
        Visualizes the circuit and highlights the critical path.

        Args:
            circuit (Circuit): The Circuit object.
            critical_path (list): List of node IDs in the critical path.
            output_file (str): The name of the output file (without extension).
        """
        graph = Digraph(format="png")
        graph.attr(rankdir="LR")

        critical_edges = set((critical_path[i], critical_path[i + 1]) for i in range(len(critical_path) - 1))

        for node_id, details in circuit.nodes.items():
            label = f"{node_id}\\n{details['type']}"
            shape = "ellipse" if details["type"] in ["INPUT", "OUTPUT"] else "box"
            color = "red" if node_id in critical_path else "black"
            graph.node(details["unique_id"], label=label, shape=shape, color=color)

        for node_id, details in circuit.nodes.items():
            for input_id in details["inputs"]:
                edge_color = "red" if (input_id, node_id) in critical_edges else "black"
                graph.edge(circuit.nodes[input_id]["unique_id"], details["unique_id"], color=edge_color)

        graph.render(f"./outputs/{output_file}", cleanup=True)
        print(f"Circuit visualization with critical path saved to {output_file}.png")
