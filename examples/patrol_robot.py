import sys
import os
import time
import random

# Add path to finding bindings (adjust this if running from a different directory)
sys.path.append(os.path.join(os.getcwd(), 'build', 'Release'))

try:
    import kenate_bindings
except ImportError as e:
    print(f"Error importing bindings: {e}")
    sys.exit(1)

# --- Robot Context ---
# context to fake some sensor data, nothing fancy yet
class RobotContext:
    def __init__(self):
        self.obstacle_detected = False

context = RobotContext()

# --- States ---

class PatrolState(kenate_bindings.BaseState):
    def __init__(self):
        super().__init__("Patrol")
        self.motor = kenate_bindings.MockMotor("LeftWheel")
        self.last_check = 0
        self.start_time = 0

    def on_enter(self):
        print(f"[{self.name}] Driving Forward...", flush=True)
        self.start_time = time.time()
        self.last_check = self.start_time

    def on_update(self):
        # forward at full speed
        self.motor.set_velocity(1.0)
        
        # let's pretend we have a sensor (lidar? cam?) checking stuff
        if time.time() - self.last_check > 0.5:
            # 20% chance to see a wall
            if random.random() < 0.2: 
                print(f"[{self.name}] ! OBSTACLE DETECTED !", flush=True)
                context.obstacle_detected = True
            self.last_check = time.time()

        # the engine doesn't support self-transitioning from python *inside* the loop yet
        # avoiding circular ref hell for now, so I'll just flip a flag in the context
        # and let the main loop handle the switch. simple enough.
        pass

    def on_exit(self):
        print(f"[{self.name}] Stopping patrol.", flush=True)
        self.motor.set_velocity(0.0)

class ObstacleAvoidanceState(kenate_bindings.BaseState):
    def __init__(self):
        super().__init__("Avoidance")
        self.motor = kenate_bindings.MockMotor("LeftWheel")
        self.entry_time = 0

    def on_enter(self):
        print(f"[{self.name}] Stopping and Turning...", flush=True)
        self.entry_time = time.time()
        self.motor.set_velocity(0.0) # Stop first

    def on_update(self):
        # U-turn
        self.motor.set_velocity(-0.5)
        
        # giving it 2 secs to clear the "obstacle"
        if time.time() - self.entry_time > 2.0:
            print(f"[{self.name}] Path clear.", flush=True)
            context.obstacle_detected = False

    def on_exit(self):
        print(f"[{self.name}] Resuming patrol.", flush=True)

# --- Main Logic ---

def main():
    engine = kenate_bindings.Engine()
    engine.set_frequency(100.0) # 100Hz control loop

    patrol = PatrolState()
    avoid = ObstacleAvoidanceState()

    engine.add_state(patrol)
    engine.add_state(avoid)

    # starting in patrol mode tracking
    current_mode = "Patrol"

    print("Starting Robot Engine...", flush=True)
    engine.start()

    # supervisor loop to catch those context flags
    # in a real setup, states would return the next state, but this works for now
    try:
        start_app = time.time()
        while time.time() - start_app < 15.0: # 15s should be enough for a demo
            # only switch if we actually need to change gears
            
            if context.obstacle_detected:
                 # we wanna go to Avoidance.
                 # we track current_mode so we don't spam the engine with set_state calls
                 # otherwise it resets the state (on_enter/on_exit) every 0.1s which looks glitchy
                 pass
            
            time.sleep(0.1) # slow tick for the supervisor

            # Logic check:
            # if we see a wall -> avoidance
            # if clear -> patrol
            
            desired = "Avoidance" if context.obstacle_detected else "Patrol"
            if desired != current_mode:
                engine.set_state(desired)
                current_mode = desired

    except KeyboardInterrupt:
        pass

    print("Shutting down...", flush=True)
    engine.stop()

if __name__ == "__main__":
    main()