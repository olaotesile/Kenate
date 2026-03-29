import atexit
import os
import threading
import time

"""
KENATE STANDARD LIBRARY - PHASE 1
DEVELOPED BY EURETIX LABS 2025

This module contains the pre-built "Personalities" that come with the 
Kenate framework. These classes handle common robotic logic so 
developers don't have to write them from scratch.
"""

class WaitState:
    """
    WAIT STATE (WaitState())
    Purpose: Provides precision timed pauses without blocking the control loop.
    """
    def __init__(self, duration):
        self.duration = duration
        self.start_time = time.monotonic()
        self.complete = False

    def is_complete(self):
        """Returns True if the specified duration has elapsed."""
        if not self.complete:
            if time.monotonic() - self.start_time >= self.duration:
                self.complete = True
        return self.complete

class SequenceState:
    """
    SEQUENCE STATE (SequenceState())
    Purpose: Chains multiple behaviors into a single autonomous flow.
    """
    def __init__(self, states):
        self.states = states
        self.current_index = 0
        self.active_state = None

    def execute(self, engine):
        """Progresses through the list of states automatically."""
        if self.current_index >= len(self.states):
            return True # Sequence finished

        if self.active_state is None:
            state_class = self.states[self.current_index]
            self.active_state = state_class()
            engine.add_state(self.active_state)
            engine.set_state(self.active_state.name)
            self.current_index += 1
            
        return False

class PIDState:
    """
    PID CONTROLLER STATE (PIDState())
    Purpose: Industry-standard math for smooth, precise motor positioning.
    """
    def __init__(self, p, i, d, target):
        self.kp = p
        self.ki = i
        self.kd = d
        self.target = target
        
        self.prev_error = 0
        self.integral = 0
        self.last_time = time.monotonic()

    def calculate(self, current_value):
        """Returns the required motor correction based on PID math."""
        now = time.monotonic()
        dt = now - self.last_time
        if dt <= 0: dt = 0.001 # Prevent division by zero
        
        error = self.target - current_value
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        
        self.prev_error = error
        self.last_time = now
        return output

class ThresholdState:
    """
    THRESHOLD STATE (ThresholdState())
    Purpose: Triggers transitions based on sensor value ranges.
    """
    def __init__(self, min, max):
        self.min_val = min
        self.max_val = max

    def is_below_minimum(self, value):
        """Returns True if value is under the minimum threshold."""
        return value < self.min_val

    def is_above_maximum(self, value):
        """Returns True if value is above the maximum threshold."""
        return value > self.max_val

class BlackBoxLogger:
    """
    BLACK BOX LOGGER (BlackBoxLogger())
    Purpose: Captures high-frequency (1000Hz) telemetry data for analysis.
    """
    def __init__(self, filename="mission_log.csv", flush_interval=0.5, buffer_size=256):
        self.filename = filename
        self.log_dir = ".kenate_logs"
        self.path = os.path.join(os.getcwd(), self.log_dir, self.filename)
        self.flush_interval = flush_interval
        self.buffer_size = buffer_size
        self._buffer = []
        self._last_flush = time.monotonic()
        self._lock = threading.Lock()
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # Initialize the log file with headers
        self._file = open(self.path, 'w', buffering=1)
        self._file.write("timestamp,state,height,distance,battery,temp,signal\n")
        atexit.register(self.close)

    def log(self, state_name, sensors):
        """Writes a single entry to the telemetry log."""
        timestamp = time.monotonic()
        data = f"{timestamp},{state_name},{sensors['height']},{sensors['distance']},{sensors['battery']},{sensors['temp']},{sensors['signal']}\n"
        with self._lock:
            self._buffer.append(data)
            now = time.monotonic()
            if len(self._buffer) >= self.buffer_size or (now - self._last_flush) >= self.flush_interval:
                self._flush_locked(now)

    def _flush_locked(self, now=None):
        if not self._buffer:
            return
        if now is None:
            now = time.monotonic()
        self._file.writelines(self._buffer)
        self._buffer.clear()
        self._file.flush()
        self._last_flush = now

    def flush(self):
        with self._lock:
            self._flush_locked()

    def close(self):
        with self._lock:
            if self._file:
                self._flush_locked()
                self._file.close()
                self._file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

class WatchdogState:
    """
    WATCHDOG STATE (WatchdogState())
    Purpose: A background safety guardian that monitors system health.
    """
    def __init__(self, timeout=0.1):
        self.timeout = timeout
        self.last_heartbeat = time.monotonic()

    def heartbeat(self):
        """Update the heartbeat timestamp."""
        self.last_heartbeat = time.monotonic()

    def check_health(self):
        """Returns False if a timeout has occurred."""
        return (time.monotonic() - self.last_heartbeat) < self.timeout

def default_safety_check(state, max_temp=85.0, min_battery=20.0, min_signal=20.0):
    if state is None:
        return True
    return (
        state.get_system_temperature() <= max_temp
        and state.get_battery_level() >= min_battery
        and state.get_signal_strength() >= min_signal
    )
