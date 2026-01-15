import kenate_bindings as _kb
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

class Robot:
    def __init__(self, port=None):
        self._engine = _kb.Engine()
        self.port = port
        self._states = {}

    def create_state(self, name, state_cls=None):
        if state_cls is None:
            # Create a simple generic state if none provided
            class GenericState(BaseState):
                def on_update(self): pass
            state_cls = GenericState
        
        state_obj = state_cls(name)
        self._engine.add_state(state_obj)
        wrapper = StateWrapper(self._engine, state_obj)
        self._states[name] = wrapper
        return wrapper

    def set_frequency(self, hz):
        self._engine.set_frequency(hz)

    def start(self):
        print(f"[Kenate] Starting Engine on {self.port or 'Simulation'}...")
        self._engine.start()

    def stop(self):
        self._engine.stop()

    def wait(self, duration_sec):
        # Utility to wait while the background engine runs
        time.sleep(duration_sec)
