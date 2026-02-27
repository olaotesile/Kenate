#include <atomic>
#include <chrono>
#include <csignal>
#include <iostream>
#include <kenate/BaseState.hpp>
#include <kenate/Engine.hpp>
#include <kenate/hal/MockMotor.hpp>

class HighFreqState : public kenate::BaseState {
public:
  HighFreqState()
      : kenate::BaseState("HighFreq"), motor_("Joint1"), count_(0) {}

  void on_enter() override {
    std::cout << "[C++] Entering HighFreq State. Target: 1000Hz" << std::endl;
    start_time_ = std::chrono::steady_clock::now();
    last_print_ = start_time_;
  }

  void on_update() override {
    count_++;
    motor_.set_velocity(1.0); // forcing the fake motor to move

    auto now = std::chrono::steady_clock::now();
    if (std::chrono::duration_cast<std::chrono::seconds>(now - last_print_)
            .count() >= 1) {
      std::cout << "[C++] Ticks over last second: " << count_
                << " | Motor Vel: " << motor_.get_velocity() << std::endl;
      count_ = 0;
      last_print_ = now;
    }
  }

  void on_exit() override {
    std::cout << "[C++] Exiting HighFreq State" << std::endl;
  }

private:
  kenate::hal::MockMotor motor_;
  int count_;
  std::chrono::steady_clock::time_point start_time_;
  std::chrono::steady_clock::time_point last_print_;
};

int main() {
  kenate::Engine engine;
  engine.set_frequency(1000.0); // 1khz loop

  auto state = std::make_shared<HighFreqState>();
  engine.add_state(state);

  std::cout << "[C++] Starting Engine..." << std::endl;
  engine.start();

  std::this_thread::sleep_for(std::chrono::milliseconds(3500));

  std::cout << "[C++] Shutting down..." << std::endl;
  engine.stop();

  return 0;
}
