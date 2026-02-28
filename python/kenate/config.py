import json
import os

"""
KENATE CONFIGURATION MANAGER
DEVELOPED BY EURETIX LABS 2025

This module handles the loading and validation of robot parameters 
from external configuration files.
"""

class ConfigLoader:
    """
    CONFIG LOADER (ConfigLoader())
    Purpose: Centralized management of robot constants and thresholds.
    """
    def __init__(self, config_path=None):
        self.data = {}
        if config_path:
            self.load(config_path)

    def load(self, path):
        """Loads a JSON configuration file."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"[ERROR] Configuration file not found: {path}")
            
        try:
            with open(path, 'r') as f:
                self.data = json.load(f)
            print(f"[SYSTEM] Configuration loaded successfully from: {os.path.basename(path)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"[ERROR] Invalid JSON in configuration file: {e}")

    def get(self, key, default=None):
        """Retrieves a parameter value."""
        return self.data.get(key, default)

    def validate(self, required_keys):
        """Ensures all critical parameters are present."""
        missing = [key for key in required_keys if key not in self.data]
        if missing:
            raise KeyError(f"[CRITICAL] Missing required configuration parameters: {', '.join(missing)}")
        return True
