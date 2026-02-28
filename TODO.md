# Project TODOs

If you're looking to contribute to Kenate, here are some areas where I could use your help.

- [x] Config Loader: Add support for loading robot configuration from JSON/YAML files.
- [x] Standard Library (`kenate.stdlib`): Added `WaitState`, `SequenceState`, and `PIDState`.
- [x] The CLI Tool: Created `kenate init` and `kenate run`.
- [x] Logging System: Added High-Frequency `BlackBoxLogger`.
- [x] Visualizer: Implemented `TerminalVisualizer` dashboard.
- [x] pip install: Created `setup.py` for global installation.

## Core (C++)
- [ ] Real Hardware Interface: Implement `MotorInterface` for actual hardware (e.g., Raspberry Pi GPIO).
- [ ] Logging System: Integrate `spdlog` to replace `std::cout`.
- [ ] Unit Tests: Set up Google Test (GTest) for C++ logic.

## Ecosystem (Encore Phase)
- [ ] Web Visualizer: React/Next.js dashboard for real-time telemetry.
- [ ] Mission Report Generator: Script to turn Black Box CSVs into performance reports.
- [ ] GitHub Actions: Automated build and test pipelines (CI/CD).
