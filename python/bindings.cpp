#include <kenate/BaseState.hpp>
#include <kenate/Engine.hpp>
#include <kenate/SafetyState.hpp>
#include <kenate/hal/MockMotor.hpp>
#include <kenate/hal/MotorInterface.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

/**
 * @brief Trampoline class for BaseState to allow Python-side inheritance.
 */
class PyBaseState : public kenate::BaseState {
public:
  using kenate::BaseState::BaseState;

  void on_enter() override {
    PYBIND11_OVERRIDE(void, kenate::BaseState, on_enter, );
  }

  void on_update() override {
    PYBIND11_OVERRIDE_PURE(void, kenate::BaseState, on_update, );
  }

  void on_exit() override {
    PYBIND11_OVERRIDE(void, kenate::BaseState, on_exit, );
  }

  float get_height_sensor() override {
    PYBIND11_OVERRIDE(float, kenate::BaseState, get_height_sensor, );
  }

  float get_distance_sensor() override {
    PYBIND11_OVERRIDE(float, kenate::BaseState, get_distance_sensor, );
  }

  float get_battery_level() override {
    PYBIND11_OVERRIDE(float, kenate::BaseState, get_battery_level, );
  }

  float get_system_temperature() override {
    PYBIND11_OVERRIDE(float, kenate::BaseState, get_system_temperature, );
  }

  float get_signal_strength() override {
    PYBIND11_OVERRIDE(float, kenate::BaseState, get_signal_strength, );
  }
};

PYBIND11_MODULE(bindings, m) {
  m.doc() = "Kenate Robotics Framework Core Bindings";

  py::class_<kenate::BaseState, PyBaseState,
             std::shared_ptr<kenate::BaseState>>(m, "BaseState")
      .def(py::init<std::string>())
      .def("on_enter", &kenate::BaseState::on_enter)
      .def("on_update", &kenate::BaseState::on_update)
      .def("on_exit", &kenate::BaseState::on_exit)
      .def("get_height_sensor", &kenate::BaseState::get_height_sensor)
      .def("get_distance_sensor", &kenate::BaseState::get_distance_sensor)
      .def("get_battery_level", &kenate::BaseState::get_battery_level)
      .def("get_system_temperature", &kenate::BaseState::get_system_temperature)
      .def("get_signal_strength", &kenate::BaseState::get_signal_strength)
      .def_property_readonly("engine", &kenate::BaseState::get_engine)
      .def_property_readonly("name", &kenate::BaseState::name);

  py::class_<kenate::Engine>(m, "Engine")
      .def(py::init<>())
      .def("add_state", &kenate::Engine::add_state)
      .def("set_state", &kenate::Engine::set_state)
      .def("start", (void (kenate::Engine::*)()) &kenate::Engine::start)
      .def("stop", &kenate::Engine::stop)
      .def("set_frequency", &kenate::Engine::set_frequency)
      .def("get_current_state", &kenate::Engine::get_current_state)
      .def("get_current_state_name", &kenate::Engine::get_current_state_name);

  py::class_<kenate::SafetyState, kenate::BaseState, std::shared_ptr<kenate::SafetyState>>(m, "SafetyState")
      .def(py::init<>());

  // --- HAL Bindings ---
  py::class_<kenate::hal::MotorInterface,
             std::shared_ptr<kenate::hal::MotorInterface>>(m, "MotorInterface")
      .def("set_velocity", &kenate::hal::MotorInterface::set_velocity)
      .def("set_position", &kenate::hal::MotorInterface::set_position)
      .def("set_effort", &kenate::hal::MotorInterface::set_effort)
      .def("get_velocity", &kenate::hal::MotorInterface::get_velocity)
      .def("get_position", &kenate::hal::MotorInterface::get_position)
      .def("get_effort", &kenate::hal::MotorInterface::get_effort)
      .def_property_readonly("name", &kenate::hal::MotorInterface::name);

  py::class_<kenate::hal::MockMotor, kenate::hal::MotorInterface,
             std::shared_ptr<kenate::hal::MockMotor>>(m, "MockMotor")
      .def(py::init<std::string>())
      .def("set_velocity", &kenate::hal::MockMotor::set_velocity)
      .def("get_velocity", &kenate::hal::MockMotor::get_velocity);
}
