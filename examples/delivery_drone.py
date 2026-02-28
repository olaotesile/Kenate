import sys
import os
import time

# --- STEP 0: THE IMPORTS (The "Ingredients") ---
# We need to find the Kenate Engine we built earlier.
# This line tells Python where to look for the 'kenate_bindings' module.
sys.path.append(os.path.join(os.getcwd(), 'build', 'Release'))

try:
    import kenate_bindings
    # From the Standard Library, we want the SafetyState.
    # Why? Because if the drone is dying, we don't want to write "Stop" logic again.
    # We want a professional-grade emergency brake ready to go.
    from kenate_bindings import SafetyState
except ImportError:
    print("Error: Kenate Engine not found. Please build the project first.")
    sys.exit(1)

# --- THE DRONE STATE MACHINE ---
# This is where the programmer defines the "Moods" of the robot.

# MOOD 1: THE ASCENT (TakeOff)
class TakeOffState(kenate_bindings.BaseState):
    def __init__(self):
        super().__init__("TakeOff")
        self.target_height = 10.0
        # Thought Process: I need a motor to push the drone up.
        self.vertical_motor = kenate_bindings.MockMotor("VerticalThruster")

    def on_enter(self):
        print("[TakeOff] Initiating lift sequence to 10m.")

    def on_update(self):
        current_h = self.get_height_sensor() # Hypothetical sensor call
        
        if current_h < self.target_height:
            # We are too low! Thrusters up.
            self.vertical_motor.set_velocity(0.8)
        else:
            # We hit 10m! Transition to "Cruise" mood.
            print("[TakeOff] Height reached. Switching to Cruise.")
            self.engine.set_state("Cruise")

# MOOD 2: THE NAVIGATION (Cruise)
class CruiseState(kenate_bindings.BaseState):
    def __init__(self):
        super().__init__("Cruise")
        self.target_height = 10.0
        self.drive_motor = kenate_bindings.MockMotor("Propeller")

    def on_update(self):
        # THOUGHT: In Cruise, I do TWO things. 1: Stay at 10m. 2: Move forward.
        
        # 1. Height Maintenance
        h = self.get_height_sensor()
        if h < 9.5: self.adjust_up()
        if h > 10.5: self.adjust_down()
        
        # 2. Forward Motion
        self.drive_motor.set_velocity(1.0) # Full speed to target
        
        # 3. SCAN FOR THREATS (Obstacles)
        # THOUGHT: If I see a bird/wall closer than 5 meters, 
        # I immediately hand off to the "Evade" specialist.
        if self.get_distance_sensor() < 5.0:
            print("[Cruise] Obstacle detected! Evading.")
            self.engine.set_state("Evade")

# MOOD 3: THE REFLEX (Evade)
class EvadeState(kenate_bindings.BaseState):
    def __init__(self):
        super().__init__("Evade")
        self.vertical_motor = kenate_bindings.MockMotor("VerticalThruster")

    def on_update(self):
        # THOUGHT: Safety first. Go UP to clear the obstacle.
        print("[Evade] Clearing obstacle by gaining altitude...")
        self.vertical_motor.set_velocity(1.0)
        
        # Once the sensor is clear, we go back to the Cruise logic.
        if self.get_distance_sensor() > 10.0:
            print("[Evade] Clear! Returning to 10m Cruise.")
            self.engine.set_state("Cruise")

# --- THE MAIN BRAIN ---

def main():
    # 1. Start the 1000Hz Engine (The "Heartbeat")
    engine = kenate_bindings.Engine()
    
    # 2. Create the "Specialists"
    takeoff = TakeOffState()
    cruise = CruiseState()
    evade = EvadeState()
    emergency = SafetyState() # Taken directly from the library
    
    # 3. Tell the Engine about them
    engine.add_state(takeoff)
    engine.add_state(cruise)
    engine.add_state(evade)
    engine.add_state(emergency)
    
    # 4. Mission Start
    print("--- KENATE DRONE MISSION START ---")
    engine.start("TakeOff")

if __name__ == "__main__":
    main()
