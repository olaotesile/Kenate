# Kenate

Kenate is a state-driven robotics framework.
It lets you declare how a robot should behave based on sensor state, while running high-performance C++ under the hood to ensure ~zero-lag execution.

Why?
Most robotics code is a mess of nested `if/else` statements. Kenate flips this by treating robot behavior as a Finite State Machine (FSM). You define the states, define the triggers, and let the C++ engine handle the real-time execution.

Features
- C++ Core: A high-speed "Pulse" engine running at 1000Hz for real-time reliability.
- Pythonic API: Clean, declarative syntax for defining transitions.
- Hardware Agnostic: Designed to run on anything from a Raspberry Pi to custom microcontrollers.
- State-Aware: Built-in telemetry to see exactly what the robot is "thinking" in real-time.

Kenate is built in layers:
1. The Engine (C++): Manages the hardware loop and memory.
2. The Abstractor (C++): Handles state transitions and priorities.
3. The Bridge (Pybind11): Exposes the power of C++ to a flexible Python interface.





Currently in early development. Building the core C++ Dispatcher.

