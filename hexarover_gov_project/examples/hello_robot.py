from kenate import Robot, BaseState
import time

"""
HELLO ROBOT MISSION
This is a standard template for verifying your Kenate installation.
"""

class GreetState(BaseState):
    def on_enter(self):
        print(f"\n[MISSION] Hello! I am '{self.name}'.")
        print("[MISSION] Starting autonomous heartbeat...")

    def on_update(self):
        # Read a sensor to prove the C++ Bridge is active
        temp = self.get_system_temperature()
        battery = self.get_battery_level()
        
        print(f"[LIVE] Temp: {temp}C | Battery: {battery}%", end='\r')
        
    def on_exit(self):
        print("\n[MISSION] Shutdown complete.")

def main():
    # 1. Initialize the Robot
    my_robot = Robot(port="SIMULATION")
    
    # 2. Add the Greeting State
    my_robot.create_state("Greeting", GreetState)
    
    # 3. Start for 3 seconds
    my_robot.start()
    time.sleep(3)
    my_robot.stop()

if __name__ == "__main__":
    main()
