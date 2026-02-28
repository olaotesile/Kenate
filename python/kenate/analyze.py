import sys
import os
import csv
import time

"""
KENATE MISSION ANALYTICS
DEVELOPED BY EURETIX LABS 2025

This tool parses the Black Box CSV logs and generates a performance 
summary for the mission.
"""

def analyze_log(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] Log file not found: {file_path}")
        return

    print(f"--- ANALYZING KENATE MISSION LOG: {os.path.basename(file_path)} ---")
    
    records = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    if not records:
        print("[WARNING] No data found in log.")
        return

    # Basic Analytics
    states = set([r['state'] for r in records])
    duration = float(records[-1]['timestamp']) - float(records[0]['timestamp'])
    
    temps = [float(r['temp']) for r in records]
    max_temp = max(temps)
    avg_temp = sum(temps) / len(temps)
    
    battery_start = float(records[0]['battery'])
    battery_end = float(records[-1]['battery'])
    consumption = battery_start - battery_end

    print(f" MISSION DURATION: {duration:.2f} seconds")
    print(f" STATES VISITED:   {', '.join(states)}")
    print(f" THERMAL PROFILE:  Max: {max_temp:.1f}C | Avg: {avg_temp:.1f}C")
    print(f" ENERGY USAGE:     {consumption:.1f}% battery consumed")
    
    if max_temp > 75:
        print(" [!] ADVISORY: System operated at high thermal levels.")
    if battery_end < 20:
        print(" [!] ADVISORY: Mission ended with critical battery.")

    print("\n--- ANALYSIS COMPLETE ---")

def main():
    # Attempt to find the latest log in the default directory
    log_dir = ".kenate_logs"
    if os.path.exists(log_dir):
        files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.csv')]
        if files:
            latest_log = max(files, key=os.path.getctime)
            analyze_log(latest_log)
        else:
            print("[INFO] No logs found in .kenate_logs. Run a mission first.")
    else:
        print("[INFO] No .kenate_logs directory found.")

if __name__ == "__main__":
    main()
