# Creating example circuit text files for testing

# Circuit 1: Simple arithmetic circuit
circuit1 = """\
# Simple Arithmetic Circuit
INPUT a
INPUT b
ADD add1 a b
MUL mul1 add1 b
OUTPUT out1 mul1
"""

# Circuit 2: Circuit with register and multiplexer
circuit2 = """\
# Circuit with Register and Multiplexer
INPUT in1
INPUT in2
INPUT select
ADD add1 in1 in2
MUX mux1 in1 add1 select
REG reg1 mux1
MUL mul1 reg1 in2
OUTPUT out1 mul1
"""

# Circuit 3: Complex circuit with multiple operations
circuit3 = """\
# Complex Circuit
INPUT x1
INPUT x2
INPUT x3
ADD add1 x1 x2
MUL mul1 add1 x3
REG reg1 mul1
ADD add2 reg1 x1
MUL mul2 add2 x2
OUTPUT y mul2
"""

# Write the circuits to text files
file_paths = ["./circuit1.txt", "./circuit2.txt", "./circuit3.txt"]
contents = [circuit1, circuit2, circuit3]

for file_path, content in zip(file_paths, contents):
    with open(file_path, "w") as f:
        f.write(content)

file_paths
