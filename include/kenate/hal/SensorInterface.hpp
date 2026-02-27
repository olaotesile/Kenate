#pragma once

#include <string>

namespace kenate {
namespace hal {

class SensorInterface {
public:
  virtual ~SensorInterface() = default;

  virtual double get_value() const = 0;
  virtual std::string name() const = 0;
};

} // namespace hal
} // namespace kenate
