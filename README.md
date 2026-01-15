# Kenate

Kenate is a state-driven robotics framework.
It lets you declare how a robot should behave based on sensor state, while running high-performance C++ under the hood to ensure ~zero-lag execution.

## Why?
Most robotics code is a mess of nested `if/else` statements. Kenate flips this by treating robot behavior as a Finite State Machine (FSM). You define the states, define the triggers, and let the C++ engine handle the real-time execution.

## Features
*   **State-over-Scripts**: Encapsulate behavior in discrete `State` classes.
*   **Deterministic Engine**: 1000Hz C++ control loop using `std::chrono::steady_clock` for precise timing.
*   **Hardware Abstraction Layer (HAL)**: Interfaces for Motors and Sensors, with Mock implementations for testing.
*   **Python Bindings**: Write high-performance States in Python (inheriting from `BaseState`) that run within the C++ engine.
*   **Header-Only Core**: Easy to integrate.

## Architecture
Kenate is built in layers:
1.  **The Engine (C++)**: Manages the hardware loop (1000Hz) and memory.
2.  **The Abstractor (C++)**: Handles state transitions and priorities.
3.  **The Bridge (Pybind11)**: Exposes the power of C++ to a flexible Python interface.

## How to Run

### 1. Build the Project
Kenate uses CMake and requires Visual Studio 2022.

```bash
mkdir build
cd build
cmake -G "Visual Studio 17 2022" ..
cmake --build . --config Release
```

### 2. Run C++ Example (Simple Loop)
The C++ example demonstrates the 1000Hz deterministic loop and HAL usage.
```bash
./build/Release/simple_loop.exe
```

### 3. Run Python Patrol Robot
The Python example demonstrates state inheritance, switching, and hardware control from Python.
```bash
python examples/patrol_robot.py
```
*Note: The script automatically adds `build/Release` to `sys.path` to find the `kenate_bindings` module.*
