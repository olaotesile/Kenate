import sys
import os
import time

# --- STEP 1: LOAD THE KERNEL AND PROFESSIONAL SUITE ---
sys.path.append(os.path.join(os.getcwd(), 'build', 'Release'))
sys.path.append(os.path.join(os.getcwd(), 'python'))

try:
    import kenate_bindings as kenate
    from kenate_stdlib import PIDState, ThresholdState, BlackBoxLogger
    from kenate_diag import TerminalVisualizer
    from kenate_config import ConfigLoader
    from kenate_bindings import SafetyState
except ImportError:
    print("Error: Kenate Framework components not found.")
    sys.exit(1)

# --- STEP 2: DYNAMIC MISSION LOGIC ---

class AutonomousMission(kenate.BaseState):
    def __init__(self, config):
        super().__init__("MissionNav")
        self.config = config
        
        # Load Dynamic Parameters from Config
        pid = config.get("PID_SETTINGS")
        safety = config.get("SAFETY")
        
        self.motor = kenate.MockMotor("MainDrive")
        self.thruster = kenate.MockMotor("VerticalThruster")
        
        # Initialize Library Components with Config values
        self.height_pid = PIDState(p=pid['P'], i=pid['I'], d=pid['D'], target=config.get("TARGET_HEIGHT"))
        self.signal_guard = ThresholdState(min=safety['MIN_SIGNAL'], max=100)
        self.thermal_guard = ThresholdState(min=0, max=safety['MAX_TEMP'])
        
        self.logger = BlackBoxLogger(filename="dynamic_mission.csv")
        self.dash = TerminalVisualizer(robot_id=config.get("ROBOT_ID"))

    def on_update(self):
        # 1. Height Control (Using Configured PID)
        h_correction = self.height_pid.calculate(self.get_height_sensor())
        self.thruster.set_velocity(h_correction)
        
        # 2. Drive (Using Configured Velocity)
        self.motor.set_velocity(self.config.get("CRUISE_VELOCITY"))
        
        # 3. Telemetry
        sensors = {
            'height': self.get_height_sensor(),
            'distance': self.get_distance_sensor(),
            'battery': self.get_battery_level(),
            'temp': self.get_system_temperature(),
            'signal': self.get_signal_strength()
        }

        # 4. Diagnostics & Logging
        self.logger.log(self.name, sensors)
        self.dash.render(self.name, sensors)

        # 5. Dynamic Safety Checks
        if self.thermal_guard.is_above_maximum(sensors['temp']):
            print(f"[SAFETY] Temperature above {self.thermal_guard.max_val}C limit!")
            self.engine.set_state("SafetyState")
            
        if self.signal_guard.is_below_minimum(sensors['signal']):
            self.engine.set_state("EmergencyLand")

class EmergencyLand(kenate.BaseState):
    def __init__(self):
        super().__init__("EmergencyLand")
        self.vertical = kenate.MockMotor("VerticalThruster")

    def on_update(self):
        self.vertical.set_velocity(-0.3)
        if self.get_height_sensor() < 0.1:
            self.engine.stop()

# --- STEP 3: SYSTEMS INITIALIZATION ---

def main():
    # 1. Load the Robot Personality
    config = ConfigLoader()
    # We point to the specific mission config in the examples folder
    config_file = os.path.join(os.getcwd(), "examples", "drone_config.json")
    config.load(config_file)
    
    # 2. Setup the Brain
    engine = kenate.Engine()
    
    engine.add_state(AutonomousMission(config))
    engine.add_state(EmergencyLand())
    engine.add_state(SafetyState())
    
    print(f"--- INITIALIZING MISSION: {config.get('MISSION_NAME')} ---")
    time.sleep(1) # Dramatic pause for systems check
    
    engine.start("MissionNav")

if __name__ == "__main__":
    main()
