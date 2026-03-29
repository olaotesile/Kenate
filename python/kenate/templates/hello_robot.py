from kenate import Robot, BaseState
import time

"""
HELLO ROBOT MISSION
Your first handshake with the engine. If this runs, your robot brain is awake.
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
    
    # 3. Start for ~5 seconds (with graceful shutdown)
    try:
        my_robot.start()
        # Keep the main thread alive while the C++ engine runs
        for _ in range(50):
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Manual interrupt detected. Safely docking...")
    finally:
        my_robot.stop()
        print("[SYSTEM] Mission Terminated. Black Box preserved.")

if __name__ == "__main__":
    main()
