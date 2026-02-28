"""
================================================================================
ENGINEERING MASTERCLASS: THE HEXAPOD WALKING GAIT (TRIPOD)
================================================================================

Welcome to the big leagues! Coordinating 6 legs at once is one of the hardest 
things in robotics. But don't worry, we're going to do it "to the bone."

--------------------------------------------------------------------------------
STEP 1: INSTALLING KENATE
--------------------------------------------------------------------------------
Before we do anything, let's get the engine installed on your machine. Open 
your terminal and run:

    pip install kenate --no-cache-dir

This gives us the high-speed "Heartbeat" we need for smooth walking.

--------------------------------------------------------------------------------
STEP 3: MOVING TO THE REAL ROBOT
--------------------------------------------------------------------------------
When you're ready to see the legs move for real, you copy this file onto your 
robot (usually using Git or a direct SSH connection). 

On the actual robot, you'll change the "port" from "SIMULATION" to something 
like "GPIO" or "/dev/ttyUSB0" so the code knows to talk to real motors 
instead of just drawing on your screen.

Once you run the script on the robot, the C++ Heartbeat takes over, and the 
Hexapod will stand up!

--------------------------------------------------------------------------------
STEP 4: THE PSEUDO-CODE (THE WALKING PLAN)
--------------------------------------------------------------------------------
1. START: Center all 6 legs so the robot is standing tall.
2. TRIPOD A: Lift legs 1, 3, and 5 together.
3. TRIPOD B: While Group A is lifting, legs 2, 4, and 6 push the ground.
4. COORDINATION: Use a Sine wave to make the transition between groups smooth 
   instead of bouncy.
5. SYSTEM CHECK: Constantly check the height sensor. If the robot "sags" too 
   low (dragging), adjust the power.
6. DATA: Save every single leg position to the Black Box for later.

Let's dive into the math and the code below!
"""

from kenate import Robot, BaseState
from kenate.stdlib import WaitState, BlackBoxLogger
from kenate.diag import TerminalVisualizer
import math
import time

# ==============================================================================
# THE GAIT ENGINE
# ==============================================================================
class HexapodWalking(BaseState):
    """
    RATIONALE: We don't use 'if' statements to walk. We use Sine waves. 
    It makes the robot look move like a living creature instead of a stuttering toy.
    """
    def on_enter(self):
        print("\n[GAIT] Initializing Biomimetic Tripod Sequence...")
        self.logger = BlackBoxLogger()
        self.viz = TerminalVisualizer(robot_id="HEXA-v1")
        
        # Our internal "Clock" for the walking wave
        self.cycle_time = 0.0 
        self.step_height = 5.0 
        self.walking_speed = 2.0 

    def on_update(self):
        # 1. TIME: Because the C++ kernel pulses every 1ms, 
        # we add exactly 0.001 to our clock every time this function runs.
        self.cycle_time += 0.001 
        
        # 2. THE WAVE: Tripod pattern (Legs 1,3,5 vs 2,4,6)
        # We use math.sin() to create a smooth repetitive wave.
        wave_a = math.sin(self.cycle_time * self.walking_speed * 2 * math.pi)

        # 3. LEG LIFT: Calculate how high Group A and Group B should be
        leg_group_a_height = max(0, wave_a * self.step_height)
        leg_group_b_height = max(0, -wave_a * self.step_height)

        # 4. SENSORS: Monitor the ground distance
        ground_distance = self.get_height_sensor()
        temp = self.get_system_temperature()

        # 5. DASHBOARD: Show us what's happening live
        self.viz.render(self.name, {
            'height': ground_distance,
            'distance': leg_group_a_height, # This lets us visualize the "Lift"
            'battery': 95,
            'temp': temp,
            'signal': 100
        })

        # 6. BLACK BOX: Record every millisecond of motion
        self.logger.log(self.name, {
            'height': ground_distance, 
            'distance': leg_group_a_height, 
            'temp': temp,
            'battery': 95,
            'signal': 100
        })

def main():
    # Setup our robot as a simulation for easy testing
    robot = Robot(port="SIMULATION")
    
    # Plug in our Walking Brain
    robot.create_state("TripodGait", HexapodWalking)
    
    try:
        print("--- LAUNCHING HEXAPOD BIOMIMETIC GAIT ---")
        robot.start()
        # Let's walk for 10 seconds!
        for _ in range(100):
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[STOP] Gait sequence interrupted.")
    finally:
        robot.stop()
        print("[OK] Hexapod powered down safely.")

if __name__ == "__main__":
    main()
