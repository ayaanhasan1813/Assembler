# assembler and simulator

This project is a simple simulator and assembler for a hypothetical assembly language, created as part of the CSE 112 - Computer Organisation course. The project includes functionality to read assembly code from a file or standard input, parse and translate it into machine code, and handle various errors that may arise during the process.

# Features

**Assembly Code Input:** Accepts assembly code through a text file or standard input.

**Error Handling**: Checks for syntax errors, invalid immediate values, undefined variables/labels, and other common issues.

**Binary Code Output:** Translates assembly code into binary machine code and outputs it to a file (output.txt) and the terminal.

**Simulation:** Simulates the execution of the assembly instructions.


# Instructions
Input
You can provide the input assembly code in two ways:
Standard Input: Uncomment the following lines in the script to read input from standard input:


import sys
code = sys.stdin.read().splitlines()
Text File: Provide the path to the text file containing the assembly code and uncomment the following lines:


with open('t.txt') as file1:
    code = file1.read().splitlines()
Output
The output binary code will be written to output.txt and also displayed in the terminal. Ensure you have write permissions for the directory where the script is located.

# Running the Script
Ensure all dependencies are installed:

No external libraries are required.
Make sure Python is installed on your system.

Execute the Script:

If using standard input, run the script and provide the assembly code input directly.
If using a text file, ensure the file path is correct and run the script.

# Error Handling
The script performs extensive error checking, including:

> Invalid immediate values (non-numeric or out of range).
> Invalid register names.
> Undefined variables or labels.
> Multiple declarations of variables or labels.
> Missing hlt instruction or hlt not at the end.
> Illegal use of the FLAGS register.
> Sufficient parameters for each operation.
> If any errors are found, the script will print an appropriate error message and terminate.

# Code Structure
The script is divided into the following main sections:

# Input Handling: Reading assembly code from either standard input or a text file.
**Data Structures:**

> RegAddress: Maps register names to their binary codes.
> operations: Maps operation mnemonics to their binary opcodes and instruction formats.
> labels, var: Lists to store labels and variables.

**Error Handling:** 
Checks for various types of errors in the assembly code.

**Assembler Logic:**
Parsing the assembly code and converting it into binary machine code.
Handling labels and variables appropriately.

**Output: **
Writing the generated binary code to output.txt and displaying it in the terminal.

# Example
An example of an assembly input file (t.txt):
assembly
var x
add R1 R2 R3
mov R4 $5
st R1 x
hlt


# To run the script with this input file, ensure the following lines are uncommented in the script:

python
with open('t.txt') as file1:
    code = file1.read().splitlines()
Execute the script and check output.txt for the resulting binary code.


# Group Members
Aditya Sharma (2022038)
Ayan Kumar Singh (2022122)
Ayaan Hasan (2022121)
Kanishk Kumar Meena (2022233)

#License
This project is created for educational purposes as part of the CSE 112 course. Feel free to use and modify it for similar educational use cases
