#pragma once

#include <string>

namespace kenate {
namespace hal {

class MotorInterface {
public:
  virtual ~MotorInterface() = default;

  virtual void set_velocity(double velocity) = 0;
  virtual void set_position(double position) = 0;
  virtual void set_effort(double effort) = 0;

  virtual double get_velocity() const = 0;
  virtual double get_position() const = 0;
  virtual double get_effort() const = 0;

  virtual std::string name() const = 0;
};

} // namespace hal
} // namespace kenate
