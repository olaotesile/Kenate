# Kenate Framework: API Reference & Specification

This document defines the complete surface area of the Kenate Framework.

## 1. The Standard Library (`kenate.stdlib`)
Pre-built states available to every developer out of the box.

*   `WaitState(duration_seconds: float, next_state: str = None)`
    *   **Purpose**: Do nothing for `duration_seconds`.
    *   **Behavior**: Optionally transitions to `next_state` when done. If `next_state` is None, it transitions to the *previous* state (acts as a pause).
*   `SequenceState(states: List[BaseState])`
    *   **Purpose**: Execute a linear chain of states.
    *   **Example**: `SequenceState([MoveToDoor(), OpenDoor(), MoveThrough()])`
*   `StopState()`
    *   **Purpose**: Safety shutdown. Sets all motors to 0. Cannot exit this state unless manually forced by the Engine.
*   `ParallelState(states: List[BaseState])`
    *   **Purpose**: Run multiple states simultaneously.
    *   **Behavior**: Calls `on_update()` on *all* child states. Transitions only when *all* children have finished.
*   `LogState(message: str, level: str = "INFO")`
    *   **Purpose**: One-shot state that logs a message and immediately returns to previous state. Useful for debugging chains.

## 2. BaseState API (`kenate.BaseState`)
Every state you write inherits these methods.

### Lifecycle Methods (Overridable)
*   `on_enter(self)`: Called exactly once when the state becomes active. Use for setup.
*   `on_update(self)`: Called every tick (1000Hz). **Cannot block.**
*   `on_exit(self)`: Called exactly once before the state is removed. Use for cleanup.

### Motion Methods (The "Act" methods)
*   `self.set_motor_speed(motor_id: int, speed: float)`: Set speed (-100.0 to 100.0).
*   `self.set_servo_angle(servo_id: int, angle: float)`: Set absolute angle (0-180).
*   `self.stop_all_motors()`: Sets all registered motors to 0 immediately.

### Sensing Methods (The "Sense" methods)
*   `self.get_distance(sensor_id: int) -> float`: Returns distance in cm.
*   `self.get_encoder(motor_id: int) -> int`: Returns raw encoder ticks.
*   `self.get_battery_voltage() -> float`: Returns system voltage.
*   `self.get_imu_heading() -> float`: Returns compass heading (0-360).

### Flow Control
*   `self.change_state(state_name: str)`: Request immediate transition.
*   `self.get_time() -> float`: Returns seconds since Engine start (high precision).
*   `self.log(msg: str)`: Thread-safe logging to console/file.

## 3. Engine API (`kenate.Engine`)
The C++ core controller.

*   `register_state(name: str, state_instance: BaseState)`: Adds a focused behavior to the robot's brain.
*   `start(initial_state: str)`: **Blocking Call**. Starts the infinite loop.
*   `stop()`: Signals the loop to terminate cleanly.
*   `pause()`: Pauses the tick loop (keeps motors at last value).
*   `resume()`: Resumes the tick loop.
*   `get_current_state_name() -> str`: Returns the active state name.
*   `load_config(path: str)`: Loads hardware mapping (see below).

## 4. Hardware Configuration (`hardware.toml`)
Plugins are not configured in Python code (to keep it clean). They are defined in a `hardware.toml` file at the project root.

```toml
[driver]
type = "raspberry_pi" # or "odrive", "mock"

[motors]
left_wheel = { pin = 18, type = "pwm" }
right_wheel = { pin = 19, type = "pwm" }

[sensors]
front_sonar = { pin = 23, type = "hc-sr04" }
```

When you run `kenate init`, this file is created for you.

## 5. CLI Commands (`kenate`)
The developer's multitool.

*   `kenate init <project_name>`:
    *   Creates folder structure.
    *   Generates `hardware.toml`.
    *   Creates virtualenv.
*   `kenate build`:
    *   Runs CMake.
    *   Compiles C++.
    *   Links Python bindings.
*   `kenate run`:
    *   Builds (if needed) and executes `main.py`.
*   `kenate test`:
    *   Runs unit tests for your States using a detailed mock engine.
*   `kenate visualize`:
    *   Starts a local WebSocket server.
    *   Opens `localhost:3000` to show the Realtime Dashboard.

## 6. Project Structure
A standard Kenate project looks like this:

```
my_robot/
├── hardware.toml       # The hardware map
├── main.py             # Entry point
├── states/             # Your Python behaviors
│   ├── __init__.py
│   ├── patrol.py
│   ├── attack.py
│   └── idle.py
├── tests/              # Your unit tests
│   └── test_patrol.py
├── build/              # (Generated) C++ build artifacts
└── .kenate/            # (Hidden) Cache and config
```
