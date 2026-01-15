# Project TODOs

If you're looking to contribute to Kenate, here are some areas where I could use your help.

## Core (C++)
- Real Hardware Interface: Implement `MotorInterface` for actual hardware (e.g., Raspberry Pi GPIO, CAN bus, ODrive).
- Logging System: Integrate a proper logging library (like `spdlog`) to replace `std::cout` debugging.
- Unit Tests: Set up Google Test (GTest) for `Engine` and `BaseState` logic.
- Config Loader: Add support for loading robot configuration (motor IDs, PID values) from JSON/YAML files.

## Python Bindings
- Sensor Bindings: Expose `SensorInterface` to Python.
- Type Stubs: Create `.pyi` files so IDEs get autocomplete for `kenate_bindings`.
- pip install: Create a `setup.py` so the project can be installed with `pip install .`.

## Examples
- PID Controller: Create an example state that implements a PID loop for position control.
- Visualizer: Connect the Python variables to a plotting library (matplotlib) to visualize motor velocity over time. 
