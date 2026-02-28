import os
import time

"""
KENATE DIAGNOSTIC SUITE
DEVELOPED BY EURETIX LABS 2025

This module provides real-time terminal visualization for Kenate robots.
"""

class TerminalVisualizer:
    """
    TERMINAL VISUALIZER (TerminalVisualizer())
    Purpose: A live-updating console dashboard for state tracking and telemetry.
    """
    def __init__(self, robot_id="UNIT-01"):
        self.robot_id = robot_id
        self.last_update = 0

    def clear_screen(self):
        # Clears the terminal screen effectively for in-place updates
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self, state_name, sensors):
        """Renders the dashboard with the latest robot telemetry."""
        # Limit update rate to 10Hz to avoid flickering
        if time.monotonic() - self.last_update < 0.1:
            return
            
        self.clear_screen()
        print("==================================================")
        print(f"       KENATE LIVE DASHBOARD - {self.robot_id}       ")
        print("==================================================")
        print(f" TIME: {time.strftime('%H:%M:%S')} | STATUS: ACTIVE")
        print("--------------------------------------------------")
        print(f" CURRENT STATE:  [{state_name.upper()}]")
        print("--------------------------------------------------")
        print(" [ TELEMETRY ]")
        print(f" - HEIGHT:       {sensors['height']:>6.2f} m")
        print(f" - DISTANCE:     {sensors['distance']:>6.2f} m")
        print(f" - BATTERY:      {sensors['battery']:>6.0f} %")
        print(f" - CORE TEMP:    {sensors['temp']:>6.1f} C")
        print(f" - SIGNAL:       {sensors['signal']:>6.0f} %")
        print("--------------------------------------------------")
        print(" [ SYSTEM LOGS ]")
        print(f" {time.strftime('%H:%M:%S')} - Kernel executing at 1000Hz")
        if sensors['temp'] > 75:
            print(f" {time.strftime('%H:%M:%S')} - WARNING: Thermal buildup detected")
        if sensors['signal'] < 30:
            print(f" {time.strftime('%H:%M:%S')} - WARNING: Signal degradation")
        print("==================================================")
        print(" Press Ctrl+C to stop the Mission.")
        
        self.last_update = time.monotonic()
