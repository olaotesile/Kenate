from kenate import Robot, BaseState, SerialTransport, SerialMotor, SerialSensor
from kenate.stdlib import BlackBoxLogger, default_safety_check
from kenate.config import ConfigLoader
import time

"""
ARDUINO ROVER TEMPLATE
Host: Raspberry Pi / Laptop
MCU: Arduino running kenate_serial_bridge.ino
Small, brave, and easy to debug.
"""

class DriveState(BaseState):
    def __init__(self, name, left_motor, right_motor, distance_sensor, forward_speed, stop_distance):
        super().__init__(name)
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.distance_sensor = distance_sensor
        self.forward_speed = forward_speed
        self.stop_distance = stop_distance

    def on_update(self):
        dist = self.distance_sensor.read_value() or 0.0
        if dist < self.stop_distance:
            self.left_motor.set_velocity(0.0)
            self.right_motor.set_velocity(0.0)
        else:
            self.left_motor.set_velocity(self.forward_speed)
            self.right_motor.set_velocity(self.forward_speed)


def main():
    config = ConfigLoader("configs/arduino_rover.json")
    transport = SerialTransport(
        port=config.get("SERIAL", {}).get("PORT", "COM3"),
        baudrate=config.get("SERIAL", {}).get("BAUDRATE", 115200),
        timeout=0.5,
    )
    left = SerialMotor(transport, config.get("MOTORS", {}).get("LEFT", "left"))
    right = SerialMotor(transport, config.get("MOTORS", {}).get("RIGHT", "right"))
    distance = SerialSensor(transport, config.get("SENSORS", {}).get("DISTANCE", "distance"))

    robot = Robot()
    forward_speed = config.get("BEHAVIOR", {}).get("FORWARD_SPEED", 0.4)
    stop_distance = config.get("BEHAVIOR", {}).get("STOP_DISTANCE_CM", 20.0)
    state = DriveState("Drive", left, right, distance, forward_speed, stop_distance)
    robot.add_state(state)
    robot.enable_safety_monitor(default_safety_check)

    logger = BlackBoxLogger()
    try:
        robot.start()
        time.sleep(10)
    finally:
        robot.stop()
        logger.close()
        transport.close()


if __name__ == "__main__":
    main()
