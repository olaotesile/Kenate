import time
import threading

"""
KENATE BINDINGS SIMULATOR (Pure Python)
DEVELOPED BY EURETIX LABS 2025

This is a fallback module that emulates the C++ core engine.
It allows the framework to run in 'Simulation Mode' on any machine.
"""

class BaseState:
    def __init__(self, name):
        self.name = name
        self.engine = None

    def on_enter(self): pass
    def on_update(self): pass
    def on_exit(self): pass

    def get_height_sensor(self): return 10.0
    def get_distance_sensor(self): return 25.0
    def get_battery_level(self): return 88.0
    def get_system_temperature(self): return 42.0
    def get_signal_strength(self): return 95.0

class SafetyState(BaseState):
    def __init__(self):
        super().__init__("SafetyState")
    def on_enter(self):
        print("[SIMULATOR] !!! SAFETY LOCK ENGAGED !!!")

class Engine:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.pending_state_name = None
        self.running = False
        self.frequency = 1000
        self.thread = None
        self._lock = threading.Lock()

    def add_state(self, state):
        with self._lock:
            state.engine = self
            self.states[state.name] = state
            if not self.current_state:
                self.current_state = state

    def set_state(self, name):
        with self._lock:
            if name in self.states:
                self.pending_state_name = name

    def set_frequency(self, hz):
        self.frequency = hz

    def get_current_state(self):
        with self._lock:
            return self.current_state

    def get_current_state_name(self):
        with self._lock:
            return self.current_state.name if self.current_state else ""

    def start(self, initial_state=None):
        if initial_state:
            self.set_state(initial_state)
        
        self.running = True
        self.thread = threading.Thread(target=self._loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _loop(self):
        print(f"[SIMULATOR] Starting {self.frequency}Hz Python Heartbeat...")
        with self._lock:
            current_state = self.current_state
        if current_state:
            current_state.on_enter()

        interval = 1.0 / self.frequency
        next_tick = time.time()

        while self.running:
            # Handle State Transition
            exit_state = None
            enter_state = None
            with self._lock:
                if self.pending_state_name:
                    if self.current_state:
                        exit_state = self.current_state
                    self.current_state = self.states[self.pending_state_name]
                    self.pending_state_name = None
                    enter_state = self.current_state

                current_state = self.current_state

            if exit_state:
                exit_state.on_exit()
            if enter_state:
                enter_state.on_enter()

            # Tick
            if current_state:
                current_state.on_update()

            next_tick += interval
            sleep_time = next_tick - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)

class MotorInterface:
    def __init__(self, name):
        self.name = name
        self.velocity = 0.0

    def set_velocity(self, v): self.velocity = v
    def get_velocity(self): return self.velocity

class MockMotor(MotorInterface):
    def __init__(self, name):
        super().__init__(name)
