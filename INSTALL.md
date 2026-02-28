# KENATE INSTALLATION GUIDE (v1.0)
Welcome to Euretix Labs. Follow these steps to transform your machine into a high-performance robotics workstation.

## 1. PRE-REQUISITES
Ensure your system has the following installed:
- **Python 3.7+**
- **CMake (3.12+)**
- **C++ Compiler** (GCC for Linux/RPi, MSVC for Windows)

## 2. GET THE SOFTWARE
Kenate is distributed via the Euretix Labs GitHub repository.
```bash
git clone https://github.com/euretix/kenate.git
cd kenate
```

## 3. THE GLOBAL INSTALL (PyPI)
Kenate is now a globally registered framework on the [Python Package Index](https://pypi.org/project/kenate/). You can install the framework and the `kenate` CLI tool instantly with one command from any terminal:
```bash
pip install kenate
```
*(Note: For advanced hardware optimization, you may still follow the C++ build process below).*

## 4. BUILD THE HIGH-SPEED BRIDGE
Because Kenate uses a 1000Hz C++ Heart, you must compile the Hardware Bridge for your specific machine.
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

---
**SUPPORT**: If you encounter issues with the C++ build, refer to **Section VII: Hardware Abstraction** in the full [Technical Manual](./KENATE_MANUAL.txt).
