#pragma once

#include "MotorInterface.hpp"
#include <iostream>
#include <string>

namespace kenate {
namespace hal {

class MockMotor : public MotorInterface {
public:
  explicit MockMotor(std::string name)
      : name_(std::move(name)), velocity_(0.0), position_(0.0), effort_(0.0) {}

  void set_velocity(double velocity) override {
    velocity_ = velocity;
    // Simulate simple integration for position
    position_ += velocity_ * 0.001; // Assuming 1kHz loop approximately
    // std::cout << "[MockMotor:" << name_ << "] Set Velocity: " << velocity <<
    // std::endl;
  }

  void set_position(double position) override {
    position_ = position;
    // std::cout << "[MockMotor:" << name_ << "] Set Position: " << position <<
    // std::endl;
  }

  void set_effort(double effort) override {
    effort_ = effort;
    // std::cout << "[MockMotor:" << name_ << "] Set Effort: " << effort <<
    // std::endl;
  }

  double get_velocity() const override { return velocity_; }
  double get_position() const override { return position_; }
  double get_effort() const override { return effort_; }

  std::string name() const override { return name_; }

private:
  std::string name_;
  double velocity_;
  double position_;
  double effort_;
};

} // namespace hal
} // namespace kenate
