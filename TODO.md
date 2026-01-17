# Project TODOs

If you're looking to contribute to Kenate, here are some areas where I could use your help.

## Core (C++)
- Real Hardware Interface: Implement `MotorInterface` for actual hardware (e.g., Raspberry Pi GPIO, CAN bus, ODrive).
- Logging System: Integrate a proper logging library (like `spdlog`) to replace `std::cout` debugging.
- Unit Tests: Set up Google Test (GTest) for `Engine` and `BaseState` logic.
- Config Loader: Add support for loading robot configuration (motor IDs, PID values) from JSON/YAML files.

Python Bindings
- Sensor Bindings: Expose `SensorInterface` to Python.
- Type Stubs: Create `.pyi` files so IDEs get autocomplete for `kenate_bindings`.
- pip install: Create a `setup.py` so the project can be installed with `pip install .`.

## Examples
- PID Controller: Create an example state that implements a PID loop for position control.
- Visualizer: Connect the Python variables to a plotting library (matplotlib) to visualize motor velocity over time. 

## Ecosystem
These are the big ones I really want to see. If you build these, you are a legend.

- Standard Library (`kenate.stdlib`): 
  *   We need a `WaitState` so I don't have to write a timer every time."
  *   A `SequenceState` to chain stuff would also be a good one.

- The CLI Tool: 
  *   Can someone make a `kenate init` command that just sets up CMake so they can just run the command"

- The Visualizer: 
  *   I was also thinking we just add a way to see the robot's brain in a web browser. React dashboard showing current state + motor graphs? somebody please please make this happen

- Hardware Plugins: 
  *   "I need this to run on my Raspberry Pi without rewriting everything. `kenate-gpio` anyone?"
