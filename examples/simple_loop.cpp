#include <atomic>
#include <csignal>
#include <iostream>
#include <kenate/BaseState.hpp>
#include <kenate/Engine.hpp>


class CountingState : public kenate::BaseState {
public:
  CountingState() : kenate::BaseState("Counting"), count(0) {}

  void on_enter() override {
    std::cout << "[C++] Entering Counting State" << std::endl;
  }

  void on_update() override {
    count++;
    std::cout << "[C++] Count: " << count << std::endl;
    if (count >= 10) {
      std::cout << "[C++] Finished reaching 10. Stopping engine..."
                << std::endl;
      // In a real scenario, we'd trigger a transition or external stop
    }
  }

  void on_exit() override {
    std::cout << "[C++] Exiting Counting State" << std::endl;
  }

private:
  int count;
};

int main() {
  kenate::Engine engine;
  engine.set_frequency(10.0); // 10Hz

  auto counting_state = std::make_shared<CountingState>();
  engine.add_state(counting_state);

  std::cout << "[C++] Starting Engine at 10Hz..." << std::endl;
  engine.start();

  // Sleep for 1.5 seconds to allow the counter to hit 10 and then some
  std::this_thread::sleep_for(std::chrono::milliseconds(1500));

  std::cout << "[C++] Shutting down..." << std::endl;
  engine.stop();

  return 0;
}
