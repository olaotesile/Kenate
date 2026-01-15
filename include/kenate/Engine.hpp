#pragma once

#include "BaseState.hpp"
#include <atomic>
#include <chrono>
#include <iostream>
#include <map>
#include <memory>
#include <thread>

namespace kenate {

class Engine {
public:
  Engine() : running_(false), frequency_hz_(100) {}
  ~Engine() { stop(); }

  void add_state(std::shared_ptr<BaseState> state) {
    states_[state->name()] = state;
    if (!current_state_) {
      current_state_ = state;
    }
  }

  void set_state(const std::string &name) {
    auto it = states_.find(name);
    if (it != states_.end()) {
      pending_state_ = it->second;
    }
  }

  void start() {
    if (running_)
      return;
    running_ = true;

    loop_thread_ = std::thread(&Engine::run, this);
  }

  void stop() {
    running_ = false;
    if (loop_thread_.joinable()) {
      loop_thread_.join();
    }
  }

  void set_frequency(double hz) { frequency_hz_ = hz; }

private:
  void run() {

    if (current_state_) {
      current_state_->on_enter();
    }

    using namespace std::chrono;
    auto interval = nanoseconds(static_cast<int64_t>(1e9 / frequency_hz_));
    auto next_wake = steady_clock::now();

    while (running_) {
      next_wake += interval;

      // Handle transitions
      if (pending_state_) {
        if (current_state_)
          current_state_->on_exit();
        current_state_ = pending_state_;
        pending_state_.reset();
        current_state_->on_enter();
      }

      // Update current state
      if (current_state_) {
        current_state_->on_update();
      }

      std::this_thread::sleep_until(next_wake);
    }

    if (current_state_) {
      current_state_->on_exit();
    }
  }

  std::atomic<bool> running_;
  double frequency_hz_;
  std::shared_ptr<BaseState> current_state_;
  std::shared_ptr<BaseState> pending_state_;
  std::map<std::string, std::shared_ptr<BaseState>> states_;
  std::thread loop_thread_;
};

} // namespace kenate
