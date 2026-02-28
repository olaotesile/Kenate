"""
================================================================================
ENGINEERING MASTERCLASS: THE AUTONOMOUS DELIVERY ROBOT (WAREHOUSE SUITE)
================================================================================

Hey there! Welcome to your first masterclass. Instead of just looking at code, 
let's walk through how we actually build this thing from scratch, step-by-step.

--------------------------------------------------------------------------------
STEP 1: INSTALLING THE TOOLS
--------------------------------------------------------------------------------
The first step is to install Kenate. We do that by running this command in your 
terminal:

    pip install kenate --no-cache-dir

Once that's done, you'll have the "kenate" command ready to go!

--------------------------------------------------------------------------------
STEP 2: CREATING THE WORKSPACE
--------------------------------------------------------------------------------
Next, we need a professional folder to work in. Run these:

    kenate init WarehouseBot
    cd WarehouseBot

Now, let's look at the "Pseudo-Code" (the plan) before we write the real lines.

--------------------------------------------------------------------------------
STEP 4: DEPLOYING TO THE PHYSICAL MACHINE
--------------------------------------------------------------------------------
At some point, you have to move the code from your laptop to the real robot 
(like a Raspberry Pi). Most engineers do this by using a tool called "SSH" or 
just by putting the code on a USB stick or GitHub. 

Once the code is on the robot, you simply run:

    kenate run src/delivery_bot.py

Then, the Python script "wakes up" the C++ engine inside the robot's brain, 
and the navigation begins!

Now, let's look at the "Pseudo-Code" (the plan) before we write the real lines.
"""

from kenate import Robot, BaseState
from kenate.stdlib import SequenceState, WaitState, BlackBoxLogger, PIDState
from kenate.diag import TerminalVisualizer
import time

# ==============================================================================
# PHASE 1: THE SAFETY LAYER (EMERGENCY LOCKDOWN)
# ==============================================================================
# In a professional robot, we want a "Safe Zone" we can jump to if things break.
class SafetyLockdown(BaseState):
    def on_enter(self):
        print("\n[CRITICAL] EMERGENCY LOCKDOWN TRIGGERED.")
        print("[CRITICAL] Cutting power to all actuators.")
        # This is where you would send a command to kill the motors for real.
    
    def on_update(self):
        # We stay here forever until a human resets the robot.
        pass

# ==============================================================================
# PHASE 2: THE STARTUP AUDIT (BATTERY CHECK)
# ==============================================================================
# We don't want a robot dying in the middle of a hallway. We check power first.
class BatteryCheck(BaseState):
    def on_enter(self):
        self.logger = BlackBoxLogger()
        print("[SYSTEM] Performing Pre-Flight Energy Audit...")

    def on_update(self):
        battery = self.get_battery_level()
        # We record this check in the Black Box so we have proof it happened.
        self.logger.log(self.name, {'battery': battery, 'temp': self.get_system_temperature()})
        
        if battery > 20:
            print(f"[OK] Battery at {battery}%. Proceeding to Delivery.")
            self.transition_to("Navigation")
        else:
            print("[WARN] Critical Battery. Aborting mission.")
            self.transition_to("SafetyLockdown")

# ==============================================================================
# PHASE 3: THE HEARTBEAT LOOP (NAVIGATION)
# ==============================================================================
# This is where the magic happens. The C++ kernel pulses 1000 times a second.
class Navigation(BaseState):
    def on_enter(self):
        self.viz = TerminalVisualizer(robot_id="MASTER-TRANS-01")
        self.target_distance = 100.0 
        self.traveled = 0.0

    def on_update(self):
        # 1. SENSE: Gather data from the C++ Bridge
        dist_to_obstacle = self.get_distance_sensor()
        temp = self.get_system_temperature()
        battery = self.get_battery_level()
        
        # 2. THINK: Logic transitions
        if temp > 80.0:
            self.transition_to("SafetyLockdown") # Jump to safety if too hot
            return

        if dist_to_obstacle < 30:
            print("\n[ALERT] Obstacle Detected! Braking...")
            # We use a built-in state to pause for 2 seconds.
            self.transition_to("WaitState") 
            return

        # 3. ACT: Move forward and update the Dashboard
        self.traveled += 0.1 
        self.viz.render(self.name, {
            'temp': temp, 
            'battery': battery, 
            'height': 0, 
            'distance': self.traveled,
            'signal': 98
        })

        if self.traveled >= self.target_distance:
            self.transition_to("Completion")

class Completion(BaseState):
    def on_enter(self):
        print("\n[MISSION] SUCCESS! Package Delivered.")

# ==============================================================================
# PHASE 4: THE LAUNCHER
# ==============================================================================
def main():
    # We build the robot "brain" here.
    robot = Robot(port="SIMULATION")
    
    # Register our phases
    robot.create_state("StartUp", BatteryCheck)
    robot.create_state("Navigation", Navigation)
    robot.create_state("SafetyLockdown", SafetyLockdown)
    robot.create_state("Completion", Completion)
    
    try:
        # This starts the C++ 1000Hz engine!
        robot.start() 
        for _ in range(50):
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[STOP] User manual override.")
    finally:
        robot.stop() # Always stop safely
        print("[OK] System Shutdown Cleanly.")

if __name__ == "__main__":
    main()
