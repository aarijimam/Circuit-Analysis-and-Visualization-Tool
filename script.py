from circuit_class import Circuit
from visualization_class import CircuitVisualizer


def main():
    try:
        circuits = ["circuit1", "circuit2", "circuit3"]
        for circuit_name in circuits:
            circuit = Circuit(f"{circuit_name}.txt")
            CircuitVisualizer.visualize_circuit(circuit, output_file=circuit_name)
            critical_path, total_delay, components_with_delays = circuit.find_critical_path()

            print(f"Circuit: {circuit_name}")
            print(f"Critical Path: {' -> '.join(critical_path)}")
            print(f"Total Delay: {total_delay:.2f} time units")
            print("Components in Critical Path with Delays:")
            for component, delay in components_with_delays:
                print(f"  {component}: {delay:.2f} time units")

            CircuitVisualizer.visualize_with_critical_path(circuit, critical_path, output_file=f"{circuit_name}_critical_path")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
