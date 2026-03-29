try:
    from . import bindings as _kb
except ImportError:
    from . import bindings_sim as _kb
import threading
import time

class BaseState(_kb.BaseState):
    """
    Python wrapper for the C++ BaseState.
    Users can inherit from this to define your own states in Python.
    """
    def __init__(self, name):
        super().__init__(name)

    def on_enter(self):
        pass

    def on_update(self):
        pass

    def on_exit(self):
        pass

class TransitionBuilder:
    def __init__(self, source_state, target_state_name):
        self.source_state = source_state
        self.target_state_name = target_state_name
        self.condition = None

    def whenever(self, condition_func):
        self.condition = condition_func
        # In a more advanced version, i'll register this with the engine
        return self

class StateWrapper:
    def __init__(self, engine, state_obj):
        self._engine = engine
        self._state = state_obj

    def transition_to(self, target_state_name):
        # Fluent API placeholder
        return TransitionBuilder(self._state, target_state_name)

    @property
    def state(self):
        return self._state

class SafetyMonitor:
    def __init__(self, engine, check_fn, safety_state_name="SafetyState", interval=0.05):
        self._engine = engine
        self._check_fn = check_fn
        self._safety_state_name = safety_state_name
        self._interval = interval
        self._running = False
        self._thread = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def _loop(self):
        while self._running:
            try:
                state = None
                if hasattr(self._engine, "get_current_state"):
                    state = self._engine.get_current_state()
                ok = self._check_fn(state)
            except Exception:
                ok = False
            if not ok:
                self._engine.set_state(self._safety_state_name)
            time.sleep(self._interval)

class Robot:
    def __init__(self, port=None):
        self._engine = _kb.Engine()
        self.port = port
        self._states = {}
        self._watchdog = None
        self._safety_monitor = None

    def create_state(self, name, state_cls=None):
        if state_cls is None:
            # Create a simple generic state if none provided
            class GenericState(BaseState):
                def on_update(self): pass
            state_cls = GenericState

        try:
            state_obj = state_cls(name)
        except TypeError:
            state_obj = state_cls()

        self._engine.add_state(state_obj)
        wrapper = StateWrapper(self._engine, state_obj)
        self._states[name] = wrapper
        return wrapper

    def add_state(self, state_obj):
        self._engine.add_state(state_obj)
        wrapper = StateWrapper(self._engine, state_obj)
        self._states[state_obj.name] = wrapper
        return wrapper

    def set_frequency(self, hz):
        self._engine.set_frequency(hz)

    def start(self):
        print(f"[Kenate] Starting Engine on {self.port or 'Simulation'}...")
        self._engine.start()

    def stop(self):
        self._engine.stop()
        if self._safety_monitor:
            self._safety_monitor.stop()

    def wait(self, duration_sec):
        # Utility to wait while the background engine runs
        time.sleep(duration_sec)

    def current_state(self):
        if hasattr(self._engine, "get_current_state"):
            return self._engine.get_current_state()
        return None

    def enable_safety_monitor(self, check_fn, safety_state_name="SafetyState", interval=0.05):
        if self._safety_monitor:
            self._safety_monitor.stop()
        self._safety_monitor = SafetyMonitor(
            self._engine, check_fn, safety_state_name=safety_state_name, interval=interval
        )
        self._safety_monitor.start()
        return self._safety_monitor

    def attach_watchdog(self, watchdog, safety_state_name="SafetyState", interval=0.05):
        self._watchdog = watchdog
        return self.enable_safety_monitor(
            lambda _state: self._watchdog.check_health(),
            safety_state_name=safety_state_name,
            interval=interval,
        )

    def heartbeat(self):
        if self._watchdog:
            self._watchdog.heartbeat()

SafetyState = _kb.SafetyState

try:
    from .hal_serial import SerialTransport, SerialMotor, SerialSensor
except Exception:
    SerialTransport = None
    SerialMotor = None
    SerialSensor = None

try:
    from .hal_rpi import RpiGpioMotor, RpiI2CSensor
except Exception:
    RpiGpioMotor = None
    RpiI2CSensor = None

try:
    from .hal_rpi import TB6612Motor, L298NMotor
except Exception:
    TB6612Motor = None
    L298NMotor = None
