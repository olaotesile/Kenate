#include <kenate/BaseState.hpp>
#include <kenate/Engine.hpp>
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
};

PYBIND11_MODULE(kenate_bindings, m) {
  m.doc() = "Kenate Robotics Framework Core Bindings";

  py::class_<kenate::BaseState, PyBaseState,
             std::shared_ptr<kenate::BaseState>>(m, "BaseState")
      .def(py::init<std::string>())
      .def("on_enter", &kenate::BaseState::on_enter)
      .def("on_update", &kenate::BaseState::on_update)
      .def("on_exit", &kenate::BaseState::on_exit)
      .def_property_readonly("name", &kenate::BaseState::name);

  py::class_<kenate::Engine>(m, "Engine")
      .def(py::init<>())
      .def("add_state", &kenate::Engine::add_state)
      .def("set_state", &kenate::Engine::set_state)
      .def("start", &kenate::Engine::start)
      .def("stop", &kenate::Engine::stop)
      .def("set_frequency", &kenate::Engine::set_frequency);
}
