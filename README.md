KENATE ROBOTICS FRAMEWORK
The high-performance foundation for modern autonomous robotics.

Kenate is a dual-core robotics framework designed by Euretix Labs. It combines a high-speed C++17 Heart (1000Hz) with a flexible Python Soul, allowing engineers to build mission-critical autonomous systems (Drones, Rovers, Arms) in minutes, not months.

Key Features

- 1000Hz Real-Time Engine: Built in C++ for sub-millisecond control loop precision.
- Dual-Core API: Write your heavy logic in C++ and your high-level "Personalities" in Python.
- The Standard Library: Pre-built behaviors like `PIDState`, `SequenceState`, and `WaitState`.
- The Black Box: High-frequency telemetry logging for post-mission analysis.
- Universal HAL: A Hardware Abstraction Layer that runs on anything from a Laptop to a Raspberry Pi.
- Enterprise Config: Separate your robot's body data from its brain logic with JSON profiles.

 Quick Start

 1. Installation
```bash
 Clone the repository
git clone https://github.com/euretix/kenate.git
cd kenate

 Install as a professional package
pip install .
```

 2. Scaffold a New Project
```bash
kenate init MarsRover
cd MarsRover
```

 3. Run a Mission
```bash
kenate run src/mission_alpha.py
```

 Documentation

For a deep dive into the architecture, safety protocols, and API catalogs, please refer to the Official Technical Manual on Kenate's website.

  Ecosystem Status

- [x] v1.0 Core: Completed
- [x] Standard Library: Completed
- [x] CLI Toolbox: Completed
- [ ] Web Visualizer: In Development (v1.1)
- [ ] Hardware Connectors: In Development

---

Developed by Euretix Labs.
