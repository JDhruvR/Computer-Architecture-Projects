# MIPS Processor Design

This repository contains the design and implementation of a MIPS processor simulator. The simulator can execute MIPS assembly programs for calculating factorial, Fibonacci sequence, and checking if a number is prime.

## Repository Structure

- **AssemblyCodes/**: Contains sample MIPS assembly code for different programs.
  - `factorial.asm`: Assembly code to compute the factorial of a number.
  - `fibonacci.asm`: Assembly code to compute the Fibonacci sequence up to a given number.
  - `prime.asm`: Assembly code to check if a number is prime.

- **MachineCodes/**: Contains the machine code (binary representation) of the assembly programs.
  - `factorialMachineCode.txt`: Machine code for the factorial program.
  - `fibonacciMachineCode.txt`: Machine code for the Fibonacci program.
  - `primeMachineCode.txt`: Machine code for the prime-checking program.

- **Processor.py**: Python script that simulates the MIPS processor. It reads machine code and executes it, simulating the behavior of a MIPS processor.

## Usage

1. **Run the Processor Simulator**:
   Execute the `Processor.py` script to run the MIPS processor simulator. You will be prompted to choose a program and provide an input value.
   ```sh
   python Processor.py
   ```

2. **Choose a Program**:
   - Enter `1` for the factorial program.
   - Enter `2` for the Fibonacci program.
   - Enter `3` for the prime-checking program.
   - Enter any other number to exit.

3. **Provide Input**:
   Enter the input value for the chosen program when prompted.

## Files Description

### AssemblyCodes
This folder contains the MIPS assembly code for different programs.

### MachineCodes
This folder contains the machine code (binary representation) of the assembly programs.

### Processor.py

This script simulates the MIPS processor. It reads machine code and executes it, simulating the behavior of a MIPS processor.
