# Cache Simulator

## Overview

This repository contains a Cache Simulator implemented in Python. The simulator is designed to analyze cache performance metrics such as hit rate, miss rate, and hit/miss ratio under various configurations. The repository includes:

- `CacheSimulator.py`: The main Python script for the cache simulator.
- `report.pdf`: A detailed report explaining the design, implementation, and results of the cache simulator.
- `traces/`: A folder containing trace files that can be used as input for the simulator.

## Features

The cache simulator can answer the following questions:

1. **Question A**: Calculate the hit rate, miss rate, and hit/miss ratio for a given cache configuration.
2. **Question B**: Analyze how varying the cache size affects the hit rate, miss rate, and hit/miss ratio.
3. **Question C**: Analyze how varying the block size affects the hit rate, miss rate, and hit/miss ratio.
4. **Question D**: Analyze how varying the number of cache ways affects the hit rate, miss rate, and hit/miss ratio.

## Usage

### Prerequisites

- Python 3.x
- Required Python packages: `numpy`, `matplotlib`, `pandas`, `tabulate`

You can install the required packages using pip:

```bash
pip install numpy matplotlib pandas tabulate
```

### Running the Simulator

1. **Run the simulator**:

```bash
python CacheSimulator.py
```

2. **Follow the prompts**:

The simulator will prompt you to enter an integer corresponding to the question you want to analyze:

```
Enter the integer to view the corresponding answer of the question:
1) Question A [Hit rate, Miss rate, Hit/Miss ratio for the given cache]
2) Question B [Hit rate, Miss rate, Hit/Miss ratio for the given cache when the cache size is varied]
3) Question C [Hit rate, Miss rate, Hit/Miss ratio for the given cache when the block size is varied]
4) Question D [Hit rate, Miss rate, Hit/Miss ratio for the given cache when the number of cache ways is varied]
-1) Exit
```

Enter the corresponding integer to view the results for the desired question.

### Trace Files

The `traces/` folder contains trace files that can be used as input for the simulator. These trace files are referenced in the `CacheSimulator.py` script.

## Report

For a detailed explanation of the cache simulator, including design decisions, implementation details, and analysis of results, please refer to the `report.pdf` file.
