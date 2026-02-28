import sys
import os
import time

# --- STEP 1: LOAD THE KERNEL AND THE STANDARD LIBRARY ---
# We point Python to our project folders.
sys.path.append(os.path.join(os.getcwd(), 'build', 'Release'))
sys.path.append(os.path.join(os.getcwd(), 'python'))

try:
    import kenate_bindings as kenate
    # --- REAL LIBRARY IMPORTS ---
    # We are now pulling from the actual kenate_stdlib.py we just built.
    from kenate_stdlib import PIDState, ThresholdState
    # Note: SafetyState still comes from the C++ core for maximum speed.
    from kenate_bindings import SafetyState
except ImportError:
    print("Error: Kenate Core or Library not found. Please build the project.")
    sys.exit(1)

# --- STEP 2: DEFINE CUSTOM BEHAVIORS (THE PERSONALITIES) ---

# BEHAVIOR A: THE TAKEOFF SPECIALIST
class TakeOffState(kenate.BaseState):
    def __init__(self):
        super().__init__("TakeOff")
        # We use the REAL PIDState from our library now.
        self.height_controller = PIDState(p=0.5, i=0.1, d=0.01, target=10.0)
        self.thruster = kenate.MockMotor("VerticalThruster")

    def on_update(self):
        current_h = self.get_height_sensor()
        correction = self.height_controller.calculate(current_h)
        self.thruster.set_velocity(correction)

        if abs(current_h - 10.0) < 0.1:
            print("[TakeOff] Target reached. Engaging Cruise.")
            self.engine.set_state("Cruise")

# BEHAVIOR B: THE CRUISE SPECIALIST
class CruiseState(kenate.BaseState):
    def __init__(self):
        super().__init__("Cruise")
        self.forward_prop = kenate.MockMotor("MainDrive")
        self.thruster = kenate.MockMotor("VerticalThruster")
        
        # We use the REAL ThresholdState from our library.
        self.battery_guard = ThresholdState(min=15, max=100)

    def on_update(self):
        self.forward_prop.set_velocity(1.0)
        
        h = self.get_height_sensor()
        if h < 9.8: self.thruster.set_velocity(0.5)
        elif h > 10.2: self.thruster.set_velocity(-0.5)
        else: self.thruster.set_velocity(0.0)

        if self.get_distance_sensor() < 5.0:
            self.engine.set_state("Evade")
            
        if self.battery_guard.is_below_minimum(self.get_battery_level()):
            print("[Cruise] ! LOW BATTERY ! Returning home.")
            self.engine.set_state("SafetyState")

# BEHAVIOR C: THE EVADE SPECIALIST
class EvadeState(kenate.BaseState):
    def __init__(self):
        super().__init__("Evade")
        self.thruster = kenate.MockMotor("VerticalThruster")

    def on_enter(self):
        print("[Evade] Object detected. Gaining altitude to clear.")

    def on_update(self):
        self.thruster.set_velocity(1.0)
        if self.get_distance_sensor() > 10.0:
            print("[Evade] Clear. Returning to 10m height.")
            self.engine.set_state("TakeOff")

# --- STEP 3: CONSTRUCT THE DRONE'S BRAIN ---

def main():
    engine = kenate.Engine()
    
    # We create the specialists we manually built.
    takeoff = TakeOffState()
    cruise = CruiseState()
    evade = EvadeState()
    
    # We pull the safety module from the core.
    emergency_brake = SafetyState()
    
    engine.add_state(takeoff)
    engine.add_state(cruise)
    engine.add_state(evade)
    engine.add_state(emergency_brake)
    
    print("--------------------------------------------------")
    print("        EURETIX LABS: DRONE MISSION ALPHA         ")
    print("--------------------------------------------------")
    
    engine.start("TakeOff")

if __name__ == "__main__":
    main()
