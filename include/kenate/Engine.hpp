#pragma once

#include "BaseState.hpp"
#include <atomic>
#include <chrono>
#include <iostream>
#include <map>
#include <memory>
#include <mutex>
#include <thread>

namespace kenate {

class Engine {
public:
  Engine() : running_(false), frequency_hz_(1000.0) {}
  ~Engine() { stop(); }

  void add_state(std::shared_ptr<BaseState> state) {
    std::lock_guard<std::mutex> lock(mutex_);
    state->set_engine(this);
    states_[state->name()] = state;
    if (!current_state_) {
      current_state_ = state;
    }
  }

  void set_state(const std::string &name) {
    std::lock_guard<std::mutex> lock(mutex_);
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

  std::shared_ptr<BaseState> get_current_state() const {
    std::lock_guard<std::mutex> lock(mutex_);
    return current_state_;
  }

  std::string get_current_state_name() const {
    auto state = get_current_state();
    if (state) {
      return state->name();
    }
    return "";
  }

private:
  void run() {

    std::shared_ptr<BaseState> initial_state;
    {
      std::lock_guard<std::mutex> lock(mutex_);
      initial_state = current_state_;
    }
    if (initial_state) {
      initial_state->on_enter();
    }

    using namespace std::chrono;
    auto next_wake = steady_clock::now();

    while (running_) {
      auto hz = frequency_hz_.load();
      if (hz < 1.0) {
        hz = 1.0;
      }
      auto interval = nanoseconds(static_cast<int64_t>(1e9 / hz));
      next_wake += interval;

      std::shared_ptr<BaseState> state_to_update;
      std::shared_ptr<BaseState> exit_state;
      std::shared_ptr<BaseState> enter_state;
      {
        std::lock_guard<std::mutex> lock(mutex_);
        if (pending_state_) {
          exit_state = current_state_;
          current_state_ = pending_state_;
          pending_state_.reset();
          enter_state = current_state_;
        }
        state_to_update = current_state_;
      }

      if (exit_state) {
        exit_state->on_exit();
      }
      if (enter_state) {
        enter_state->on_enter();
      }

      if (state_to_update) {
        state_to_update->on_update();
      }

      auto now = steady_clock::now();
      if (now > next_wake) {
        next_wake = now;
      }
      std::this_thread::sleep_until(next_wake);
    }

    std::shared_ptr<BaseState> final_state;
    {
      std::lock_guard<std::mutex> lock(mutex_);
      final_state = current_state_;
    }
    if (final_state) {
      final_state->on_exit();
    }
  }

  std::atomic<bool> running_;
  std::atomic<double> frequency_hz_;
  std::shared_ptr<BaseState> current_state_;
  std::shared_ptr<BaseState> pending_state_;
  std::map<std::string, std::shared_ptr<BaseState>> states_;
  std::thread loop_thread_;
  mutable std::mutex mutex_;
};

} // namespace kenate
