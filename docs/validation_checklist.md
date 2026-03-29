# Kenate Host + MCU Validation Checklist

1. Firmware
Install ArduinoJson in the Arduino IDE.
Flash the correct bridge firmware from `examples/firmware/`.
For the reference profile, use Arduino + TB6612 + HC-SR04.
HC-SR04 pins (Arduino): TRIG=9, ECHO=10 (default in firmware).

2. Host Python
Install dependencies: `pip install -e .` and `pip install pyserial`.
Confirm `kenate` CLI works: `kenate --help`.

3. Serial Link
Connect MCU via USB.
Verify the port name (Windows: `COM3`, Linux: `/dev/ttyUSB0`).
Run `python tools/first_boot_check.py --port <PORT>`.

4. Motors
Confirm left motor spins for 1 second, then stops.
Confirm right motor spins for 1 second, then stops.
If direction is wrong, swap IN1/IN2 or invert in code.

5. Sensors
Confirm the distance sensor value prints.
If value is `None`, verify firmware sensor mapping.

6. Mission Run
Run `kenate init MyRover`.
Run `python examples/arduino_rover.py`.
Confirm the rover stops when the distance value is below threshold.
