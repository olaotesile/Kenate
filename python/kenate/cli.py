import os
import sys
import shutil
import argparse

"""
KENATE COMMAND LINE INTERFACE (CLI)
DEVELOPED BY EURETIX LABS 2025

The primary entry point for managing Kenate robotics projects.
"""

def init_project(name):
    print(f"--- INITIALIZING KENATE PROJECT: {name} ---")
    base_dir = os.path.join(os.getcwd(), name)
    
    # Standard Folder Structure
    folders = ["configs", "src", "examples", "python", "build", ".kenate_logs"]
    
    for folder in folders:
        path = os.path.join(base_dir, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f" [OK] Created directory: {folder}")

    # Copy templates
    package_dir = os.path.dirname(__file__)
    template_dir = os.path.join(package_dir, "templates")
    
    if not os.path.exists(template_dir):
        # Fallback for development mode
        template_dir = os.path.join(os.getcwd(), "templates")

    # 1. Robot Profile
    shutil.copy(os.path.join(template_dir, "robot_profile_template.json"), 
                os.path.join(base_dir, "configs", "default_robot.json"))
    
    # 2. Hello World Mission
    shutil.copy(os.path.join(template_dir, "hello_robot.py"), 
                os.path.join(base_dir, "examples", "hello_robot.py"))
    
    print(f" [OK] Seeded templates and example mission.")

    print(f"\nSUCCESS: Project '{name}' created. Type 'cd {name}' to begin.")

def run_mission(script_path):
    if not os.path.exists(script_path):
        print(f"[ERROR] Mission script not found: {script_path}")
        return

    print(f"--- LAUNCHING KENATE MISSION: {os.path.basename(script_path)} ---")
    
    # 1. Automatically handle mission directory
    mission_dir = os.path.dirname(os.path.abspath(script_path))
    sys.path.append(mission_dir)
    
    # 2. Execute the mission script
    # We use exec() to run the script within the current context
    with open(script_path, "r") as f:
        code = f.read()
        exec(code, {'__name__': '__main__', 'sys': sys, 'os': os})

def main():
    parser = argparse.ArgumentParser(description="Kenate Robotics Framework CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command: init
    init_parser = subparsers.add_parser("init", help="Create a new Kenate project")
    init_parser.add_argument("name", help="Name of the new project")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Execute a Kenate mission script")
    run_parser.add_argument("script", help="Path to the mission Python script")

    # Command: analyze
    analyze_parser = subparsers.add_parser("analyze", help="Generate a performance report from the last mission")

    args = parser.parse_args()

    if args.command == "init":
        init_project(args.name)
    elif args.command == "run":
        run_mission(args.script)
    elif args.command == "analyze":
        from . import analyze
        analyze.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
