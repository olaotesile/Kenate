#pragma once

#include <string>

namespace kenate {

/**
 * @brief Abstract base class for all robot states.
 * 
 * Kenate follows a "State over Scripts" philosophy. Each behavior
 * is encapsulated in a State object.
 */
class BaseState {
public:
    explicit BaseState(std::string name) : name_(std::move(name)) {}
    virtual ~BaseState() = default;

    /**
     * @brief Called once when the robot enters this state.
     */
    virtual void on_enter() {}

    /**
     * @brief Called every "tick" of the control loop (e.g., at 1000Hz).
     */
    virtual void on_update() = 0;

    /**
     * @brief Called once when the robot leaves this state.
     */
    virtual void on_exit() {}

    const std::string& name() const { return name_; }

protected:
    std::string name_;
};

} // namespace kenate
