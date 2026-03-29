KENATE ROBOTICS FRAMEWORK
The high-performance foundation for modern autonomous robotics.

Kenate is a dual-core robotics framework. It combines a C++17 engine (default 1000Hz) with a Python API for behavior so you can build real robots without the usual complexity tax.

Key Features

- 1000Hz C++ Engine: Fixed-rate loop that keeps the robot awake.
- Dual-Core API: Heavy lifting in C++, high-level behavior in Python.
- Standard Library: `PIDState`, `SequenceState`, `WaitState`, and friends.
- Black Box Logger: Telemetry for post-mission analysis.
- Universal HAL: Runs on laptops, Raspberry Pi, and anything with serial.
- Config Profiles: Separate robot body data from brain logic with JSON.

Quick Start

 1. Installation
```bash
git clone https://github.com/otesh-o/Kenate.git
cd kenate
pip install -e .
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

Host + MCU Mode (Raspberry Pi / Arduino / ESP32 / STM32)

Kenate runs on a host (Pi/Jetson/Laptop). The microcontroller handles low-level IO and listens on serial.

 1. Flash the MCU bridge
    - Arduino: `examples/firmware/kenate_serial_bridge/kenate_serial_bridge.ino`
    - ESP32: `examples/firmware/kenate_serial_bridge_esp32/kenate_serial_bridge_esp32.ino`
    - STM32 (Arduino core): `examples/firmware/kenate_serial_bridge_stm32/kenate_serial_bridge_stm32.ino`
    - Install ArduinoJson library
    - Upload to device

 2. Run the rover example
```bash
pip install pyserial
kenate init MyRover
cd MyRover
python examples/arduino_rover.py
```
Edit `configs/arduino_rover.json` for serial port and behavior (`COM3` on Windows, `/dev/ttyUSB0` on Linux).

Reference Profile
Kenate ships a reference profile: Arduino + TB6612 + HC-SR04. It is the "start here" combo.
Use `configs/arduino_rover.json` and the Arduino bridge firmware.

Raspberry Pi Host Drivers
Use the `RpiGpioMotor` and `RpiI2CSensor` classes from `kenate.hal_rpi` for GPIO/I2C.

Motor Drivers
Use `TB6612Motor` or `L298NMotor` from `kenate.hal_rpi` for common driver boards.

Validation
Run `python tools/first_boot_check.py --port <PORT>` and follow the checklist in `docs/validation_checklist.md`. It is the "trust but verify" step.

Documentation

For the deep dive, read `KENATE_MANUAL.txt`. For the friendlier walkthrough, read the Masterclass on the website.

Ecosystem Status

- [x] v1.0 Core: Completed
- [x] Standard Library: Completed
- [x] CLI Toolbox: Completed
- [ ] Web Visualizer: In Development (v1.1)
- [ ] Hardware Connectors: In Development

---

Developed by Euretix Labs.
