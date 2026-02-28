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
        self.frequency = 100
        self.thread = None

    def add_state(self, state):
        state.engine = self
        self.states[state.name] = state
        if not self.current_state:
            self.current_state = state

    def set_state(self, name):
        if name in self.states:
            self.pending_state_name = name

    def set_frequency(self, hz):
        self.frequency = hz

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
        print(f"[SIMULATOR] Starting 1000Hz Python Heartbeat...")
        if self.current_state:
            self.current_state.on_enter()

        interval = 1.0 / self.frequency
        next_tick = time.time()

        while self.running:
            # Handle State Transition
            if self.pending_state_name:
                if self.current_state:
                    self.current_state.on_exit()
                self.current_state = self.states[self.pending_state_name]
                self.pending_state_name = None
                self.current_state.on_enter()

            # Tick
            if self.current_state:
                self.current_state.on_update()

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
