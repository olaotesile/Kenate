import sys
import os
import time

# Add build/Release to path to find kenate_bindings
sys.path.append(os.path.join(os.getcwd(), 'build', 'Release'))

try:
    import kenate_bindings
    print("Successfully imported kenate_bindings")
except ImportError as e:
    print(f"Failed to import kenate_bindings: {e}")
    sys.exit(1)

class PyHighFreqState(kenate_bindings.BaseState):
    def __init__(self):
        super().__init__("PyHighFreq")
        self.count = 0
        self.last_time = time.time()

    def on_enter(self):
        print(f"[Python] Entering {self.name} State", flush=True)
        self.last_time = time.time()

    def on_update(self):
        self.count += 1
        now = time.time()
        if now - self.last_time >= 1.0:
            print(f"[Python] Ticks per second: {self.count}", flush=True)
            self.count = 0
            self.last_time = now

    def on_exit(self):
         print(f"[Python] Exiting {self.name} State", flush=True)

def main():
    engine = kenate_bindings.Engine()
    engine.set_frequency(1000.0) # Try 1000Hz
    
    state = PyHighFreqState()
    engine.add_state(state)
    
    print("[Python] Starting Engine at 1000Hz...", flush=True)
    engine.start()
    
    time.sleep(3.5)
    
    print("[Python] Stopping Engine...", flush=True)
    engine.stop()

if __name__ == "__main__":
    main()
