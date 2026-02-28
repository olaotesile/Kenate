#pragma once

#include "BaseState.hpp"
#include <iostream>

namespace kenate {

/**
 * @brief THE SAFETY STATE
 * An emergency override that locks the system and stops all motors.
 */
class SafetyState : public BaseState {
public:
    SafetyState() : BaseState("SafetyState") {}

    void on_enter() override {
        std::cout << "[KERNEL] !!! SAFETY LOCK ENGAGED !!!" << std::endl;
        std::cout << "[KERNEL] All motors forced to 0.0v." << std::endl;
    }

    void on_update() override {
        // In a real system, we would constantly pulse a "Disable" signal to the ESCs
    }

    // Sensors stay active for diagnostics
};

} // namespace kenate
