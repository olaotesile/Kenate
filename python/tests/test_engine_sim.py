import time

from kenate import BaseState, Robot, SafetyState
from kenate.stdlib import default_safety_check


class TickState(BaseState):
    def __init__(self, name):
        super().__init__(name)
        self.count = 0

    def on_update(self):
        self.count += 1


class HotState(BaseState):
    def __init__(self, name):
        super().__init__(name)

    def on_update(self):
        pass

    def get_system_temperature(self):
        return 100.0


def test_engine_ticks():
    robot = Robot()
    wrapper = robot.create_state("Tick", TickState)
    robot.set_frequency(50)
    robot.start()
    time.sleep(0.05)
    robot.stop()
    assert wrapper.state.count > 0


def test_safety_monitor_transitions():
    robot = Robot()
    robot.add_state(SafetyState())
    robot.create_state("Hot", HotState)
    robot.set_frequency(50)
    monitor = robot.enable_safety_monitor(default_safety_check, interval=0.01)
    robot.start()
    time.sleep(0.05)
    robot.stop()
    monitor.stop()
    assert robot.current_state().name == "SafetyState"
