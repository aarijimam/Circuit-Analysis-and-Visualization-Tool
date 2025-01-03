# **Circuit Analysis and Visualization Tool**

This program analyzes digital circuits, visualizes them as directed graphs, and identifies their critical paths using Object-Oriented Programming (OOP) principles.

## **Overview**

The tool reads a circuit description from a file, processes the circuit's nodes and connections, and visualizes the circuit using the `graphviz` library. It also calculates the critical path, delays, and highlights them in the visualization.

---

## **Classes**

### **1. Circuit**
Represents the circuit, including its nodes, connections, and critical path.

#### **Attributes**
- `file_path` *(str)*: Path to the circuit description file.
- `nodes` *(dict)*: A dictionary containing node details (`unique_id`, `type`, `inputs`, `outputs`).
- `inputs` *(list)*: List of input node IDs.
- `outputs` *(list)*: List of output node IDs.
- `component_delays` *(dict)*: Dictionary mapping component types to their respective delays.

#### **Methods**
1. **`__init__(file_path)`**
   - Initializes the Circuit object and reads the circuit file.
   - **Parameters**:
     - `file_path` *(str)*: Path to the circuit description file.

2. **`read_circuit()`**
   - Reads the circuit description from the file and populates the circuit attributes.
   - Handles file-related and format-related errors.
   - **Raises**:
     - `FileNotFoundError`: If the file is not found.
     - `ValueError`: If the circuit file has invalid formatting.

3. **`find_critical_path()`**
   - Calculates the critical path, total delay, and components with their delays.
   - **Returns**:
     - `critical_path` *(list)*: List of node IDs in the critical path.
     - `total_delay` *(float)*: Total delay of the critical path.
     - `components_with_delays` *(list)*: List of tuples (`node_id`, `delay`).

4. **`topological_sort()`**
   - Performs a topological sort on the circuit nodes.
   - **Returns**:
     - `sorted_nodes` *(list)*: List of node IDs in topological order.

---

### **2. CircuitVisualizer**
Handles visualization of the circuit and its critical path using the `graphviz` library.

#### **Methods**
1. **`visualize_circuit(circuit, output_file="circuit")`**
   - Visualizes the circuit as a directed graph.
   - **Parameters**:
     - `circuit` *(Circuit)*: The Circuit object to visualize.
     - `output_file` *(str, optional)*: Name of the output file (default is `"circuit"`).

2. **`visualize_with_critical_path(circuit, critical_path, output_file="circuit_with_critical_path")`**
   - Visualizes the circuit and highlights the critical path.
   - **Parameters**:
     - `circuit` *(Circuit)*: The Circuit object to visualize.
     - `critical_path` *(list)*: List of node IDs in the critical path.
     - `output_file` *(str, optional)*: Name of the output file (default is `"circuit_with_critical_path"`).

---

## **How the Program Works**

### **1. Circuit File Format**
- The circuit is described in a plain text file.
- Each line represents a node in the format:
  ```
  NODE_TYPE NODE_ID [INPUT_IDS...]
  ```
  - **NODE_TYPE**: Type of the node (e.g., `INPUT`, `OUTPUT`, `ADD`, etc.).
  - **NODE_ID**: Unique identifier for the node.
  - **INPUT_IDS** *(optional)*: IDs of input nodes connected to the current node.

### Example File:
```
# Example Circuit
INPUT A
INPUT B
ADD C A B
MUL D C A
OUTPUT E D
```

---

### **2. Program Workflow**

1. **Initialization**:
   - The `Circuit` class reads the circuit file and creates a graph structure with nodes, inputs, and outputs.
   - Handles missing files, undefined nodes, or invalid lines gracefully.

2. **Visualization**:
   - The `CircuitVisualizer` class creates a graphical representation of the circuit.
   - Nodes are styled based on their type (`ellipse` for `INPUT`/`OUTPUT`, `box` otherwise).

3. **Critical Path Analysis**:
   - The program calculates the critical path using topological sorting and delay calculations.
   - Highlights the critical path and delays in the graph.

4. **Output**:
   - The program saves visualizations as PNG files and prints critical path details to the console.

---

## **Key Functions**

### **Main Function**
Orchestrates the program flow:
1. Reads the circuit description.
2. Visualizes the circuit.
3. Finds and displays the critical path.
4. Visualizes the circuit with the critical path highlighted.

---

## **Example Usage**

### Circuit File:
`circuit1.txt`
```
INPUT A
INPUT B
ADD C A B
REG D C
OUTPUT E D
```

### Output:
1. **Console Output**:
   ```
   Circuit: circuit1
   Critical Path: A -> C -> D -> E
   Total Delay: 2.70 time units
   Components in Critical Path with Delays:
     A: 0.00 time units
     C: 1.00 time units
     D: 0.20 time units
     E: 0.50 time units
   ```

2. **Visualizations**:
   - `circuit1.png`: Graph of the circuit.
   - `circuit1_critical_path.png`: Circuit graph with the critical path highlighted in red.

---

## **Error Handling**

1. **File Not Found**:
   - Error Message: `File not found: <file_path>`

2. **Invalid Circuit File**:
   - Error Message: `Error reading circuit: <details>`

3. **Undefined Nodes**:
   - Error Message: `Undefined input node: <node_id>`

---

## **Customization**

- **Add New Node Types**:
  Modify the `component_delays` dictionary in the `Circuit` class to include new node types and their delays.

- **Change Visualization Styles**:
  Modify the `visualize_circuit` and `visualize_with_critical_path` methods in `CircuitVisualizer` to adjust colors, shapes, and styles.

---

## **Dependencies**

- **Python Libraries**:
  - `graphviz`: For visualizing the circuit.

- **Installation**:
  Install the required library using:
  ```bash
  pip install graphviz
  ```

- **Graphviz Software**:
  Ensure that the Graphviz software is installed on your system.


