# KENATE INSTALLATION GUIDE (v1.0)
Welcome to Euretix Labs. Follow these steps to turn your machine into a robotics workstation without the usual friction.

## 1. PRE-REQUISITES
Ensure your system has the following installed:
- **Python 3.7+**
- **CMake (3.12+)**
- **C++ Compiler** (GCC for Linux/RPi, MSVC for Windows)

## 2. GET THE SOFTWARE
Kenate lives here:
```bash
git clone https://github.com/otesh-o/Kenate.git
cd kenate
```

## 3. SOURCE INSTALL (LOCAL)
Install from source:
```bash
pip install -e .
```
*(Note: For advanced hardware optimization, you may still follow the C++ build process below).*

## 4. BUILD THE HIGH-SPEED BRIDGE
Because Kenate uses a fixed-rate C++ engine (default 1000Hz), you should compile the Hardware Bridge for your specific machine.
```bash
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

## 5. VERIFY INSTALLATION
Test your "Voice" (the CLI) and your "Brain" (the Engine) with one command.
```bash
# Return to the main folder
cd ..

# Run the 'Hello Robot' verification mission
kenate run examples/hello_robot.py
```

## 6. YOUR FIRST MISSION
Ready to build your own robot?
```bash
# Create your workspace
kenate init MyProject
cd MyProject

# Launch your first script
python src/your_logic.py
```

## 7. HOST + MCU (Arduino/ESP32/STM32) SETUP
This mode runs Kenate on a host (Pi/Jetson/Laptop) while a microcontroller handles low-level IO.

1. Upload the MCU bridge firmware:
   - Arduino: `examples/firmware/kenate_serial_bridge/kenate_serial_bridge.ino`
   - ESP32: `examples/firmware/kenate_serial_bridge_esp32/kenate_serial_bridge_esp32.ino`
   - STM32 (Arduino core): `examples/firmware/kenate_serial_bridge_stm32/kenate_serial_bridge_stm32.ino`
   - Install ArduinoJson library

2. Run the example mission:
```bash
pip install pyserial
kenate init MyRover
cd MyRover
python examples/arduino_rover.py
```

Edit `configs/arduino_rover.json` to match your device and behavior. This is where you make it your robot.

## 8. RASPBERRY PI HOST DRIVERS
If running on Raspberry Pi with direct GPIO/I2C, install:
```bash
pip install RPi.GPIO smbus2
```
Then use `RpiGpioMotor` and `RpiI2CSensor` from `kenate.hal_rpi`.

## 9. MOTOR DRIVERS
Kenate includes Raspberry Pi drivers for common motor boards:
- TB6612: `TB6612Motor`
- L298N: `L298NMotor`

## 10. FIRST-BOOT CHECK
Run the first-boot script and follow the validation checklist:
```bash
python tools/first_boot_check.py --port <PORT>
```
Checklist: `docs/validation_checklist.md`

---
**SUPPORT**: If you encounter issues with the C++ build, refer to **Section VII: Hardware Abstraction** in the full [Technical Manual](./KENATE_MANUAL.txt).
