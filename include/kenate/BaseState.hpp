#pragma once

#include <string>

namespace kenate {

/**
 * @brief Abstract base class for all robot states.
 * 
 * Kenate follows a "State over Scripts" philosophy. Each behavior
 * is encapsulated in a State object.
 */
class Engine; // Forward declaration

class BaseState {
public:
    explicit BaseState(std::string name) : name_(std::move(name)), engine(nullptr) {}
    virtual ~BaseState() = default;

    virtual void on_enter() {}
    virtual void on_update() = 0;
    virtual void on_exit() {}

    const std::string& name() const { return name_; }

    // --- Mock Sensors for v1.0 Autonomy ---
    virtual float get_height_sensor() { return 10.0f; }
    virtual float get_distance_sensor() { return 25.0f; }
    virtual float get_battery_level() { return 88.0f; }
    virtual float get_system_temperature() { return 42.0f; }
    virtual float get_signal_strength() { return 95.0f; }

    void set_engine(Engine* e) { engine = e; }
    Engine* get_engine() const { return engine; }

protected:
    std::string name_;
    Engine* engine;
};

} // namespace kenate
