# The Kenate Framework

## 1. What is Kenate?

Kenate is "React for Robots."

Just as React helps web developers build complex UIs by breaking them down into small, reusable Components, Kenate helps robotics developers build complex behaviors by breaking them down into small, reusable States.

Traditional Robotics:
You write one giant script (`main.py`) that tries to do everything at once. It gets messy, buggy, and hard to read.

Kenate Robotics:
You write tiny, isolated "States" (like `PatrolState`, `AttackState`, `SleepState`). Each state only cares about itself. The Kenate Engine handles switching between them.

### Key Features

1. Hybrid Power: You write easy Python code, but it runs inside a blazing-fast C++ Engine (1000Hz).
2. Deterministic: The Engine guarantees your code runs at exact intervals, critical for smooth robot motion.
3. Modular: If your robot's "Attack" behavior is broken, you only need to fix `AttackState.py`. You can't break the "Patrol" behavior by accident.

---

## 2. The Kenate Ecosystem

We provide a suite of tools to make robot development feel like modern web development.

### The Standard Library (kenate.stdlib)
Don't reinvent the wheel. We provide pre-made States for common tasks:
- `WaitState(seconds)`: Pauses the robot accurately.
- `SequenceState([StateA, StateB])`: Chains behaviors together automatically.
- `StopState()`: Emergency brake that locks motors.

### The CLI (kenate)
Spin up new projects in seconds, just like `create-react-app`.
- `kenate init my_robot`: Creates your project structure.
- `kenate build`: Handles all the C++ compilation for you.

### The Visualizer
A real-time dashboard (running in your browser) that connects to your robot.
- See exactly which State is active.
- Graph motor speeds and sensor data in real-time.
- Debug transitions visually.

### Hardware Plugins
Switch hardware by changing one line of configuration, not your code.
- `kenate-raspberry-pi`: For GPIO control.
- `kenate-odrive`: For high-performance brushless motors.
- `kenate-serial`: For Arduino/Teensy communication.

---

## 3. How Does It Work?

Kenate is a "Sandwich" of technologies.

### Layer 1: The Engine (The "Brain") - C++
At the very bottom, we have a C++ program called The Engine.
It is a precise clock. It wakes up exactly 1000 times every second.
It holds the "Truth" of the robot: "What state am I in right now?"
It talks to the hardware (Motors, Sensors).

### Layer 2: The Bridge - Pybind11
This is the "Translator." It allows the C++ Engine to talk to Python.
When the Engine ticks, it asks: "Hey Python, we are in PatrolState. What should we do?"
It runs your Python code instantly and then reports back to C++.

### Layer 3: The Behaviors (The "Instructions") - Python
This is where YOU work.
You simply write Python classes.
You don't worry about "Main Loops" or "Timing" or "Memory Management."
You just say: "If I am in PatrolState, move forward."

---

## 4. How Would Someone Use It?

Imagine you want to build a robot that monitors a warehouse. Here is the step-by-step process.

### Step 1: Design Your States
Grab a pen and paper. Draw bubbles for each behavior your robot needs.
- Start: "Stand Still"
- Patrol: "Move along the path"
- Alert: "Flash lights and sound alarm"

### Step 2: Write the Python Code
For each bubble, you write one small Python class.

File: `my_robot_states.py`

```python
import kenate
from kenate.stdlib import WaitState # Use the standard library!

# Behavior 1: Just stand still
class IdleState(kenate.BaseState):
    def on_enter(self):
        print("System Online. Waiting.")
        self.set_motor_speed(0)

# Behavior 2: Patrol the area
class PatrolState(kenate.BaseState):
    def on_update(self):
        # Move forward
        self.set_motor_speed(50)
        
        # If we see something, switch to ALERT mode immediately!
        if self.get_distance_sensor() < 50:
            self.engine.change_state("AlertState")

# Behavior 3: Panic!
class AlertState(kenate.BaseState):
    def on_enter(self):
        print("INTRUDER DETECTED!")
        
    def on_update(self):
        # Stop and spin crazy
        self.set_motor_speed(-100)
```

### Step 3: Launch the Engine
You create a tiny script to load your states and hit the "Start" button.

File: `main.py`

```python
import kenate
from my_robot_states import IdleState, PatrolState, AlertState

# 1. Create the C++ Engine
engine = kenate.Engine()

# 2. Register your states (Give them names)
engine.register_state("Idle", IdleState())
engine.register_state("Patrol", PatrolState())
engine.register_state("Alert", AlertState())

# 3. Start the engine in 'Idle' mode. 
# The C++ core takes over from here!
engine.start("Idle")
```

---

## 5. Installation Guide

This is a developer framework, so it requires compiling the C++ core once.

### Prerequisites
- Windows: Visual Studio 2022 (Community Edition is free).
- Python: Version 3.8 or newer.
- CMake: A tool to build C++ projects.

### Step-by-Step Setup

1. Download the Code
   ```bash
   git clone https://github.com/olaotesile/kenate.git
   cd kenate
   ```

2. Prepare the Build
   Create a folder to hold the compiled files.
   ```bash
   mkdir build
   cd build
   ```

3. Configure
   Run CMake to find your compilers and Python version.
   ```bash
   cmake -G "Visual Studio 17 2022" ..
   ```

4. Compile
   Build the C++ Engine and generate the Python library (`kenate_bindings.pyd`).
   ```bash
   cmake --build . --config Release
   ```

5. Run
   You are ready! Run your Python script.
   ```bash
   cd ..
   python examples/patrol_robot.py
   ```
