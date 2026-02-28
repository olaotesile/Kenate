import os
import sys

# The engineer just writes their mission logic here
from kenate import Robot, BaseState
from kenate_hal import GPIOMotor
from kenate_config import ConfigLoader

class MoveToShelf(BaseState):
    def on_enter(self):
        print("[ROVER] Driving to Shelf A-4...")
        # Use physical motors from the HAL
        self.left_motor = GPIOMotor("LeftWheel", 17, 27)
        self.right_motor = GPIOMotor("RightWheel", 22, 23)

    def on_update(self):
        # Read a sensor value (exposed from C++ Core)
        dist = self.get_distance_sensor()
        
        if dist > 1.0:
            self.left_motor.set_velocity(0.5)
            self.right_motor.set_velocity(0.5)
        else:
            print("[ROVER] Target reached!")
            self.left_motor.stop()
            self.right_motor.stop()
            # Transition to the next state
            self.engine.set_state("ScanBarcode")

def main():
    # 1. Load the Rover Profile
    config = ConfigLoader()
    config.load("configs/rover_01.json")

    # 2. Boot the Robot
    my_rover = Robot(port="ROVER_PI_01")
    
    # 3. Add the custom behavior
    my_rover.create_state("Driving", MoveToShelf)
    my_rover.create_state("ScanBarcode") # Placeholder

    # 4. Start Mission
    my_rover.start()

if __name__ == "__main__":
    main()
