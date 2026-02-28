"""
KENATE HARDWARE ABSTRACTION LAYER (HAL)
DEVELOPED BY EURETIX LABS 2025

This module provides the interface between the Kenate software brain 
and physical robotic hardware (Raspberry Pi, Arduino, Jetson).
"""

class BaseHardware:
    """
    Base class for all hardware drivers.
    """
    def __init__(self, name):
        self.name = name
        self.is_connected = False

    def connect(self):
        print(f"[HAL] Connecting to hardware: {self.name}...")
        self.is_connected = True

    def disconnect(self):
        print(f"[HAL] Disconnecting: {self.name}.")
        self.is_connected = False

class GPIOMotor(BaseHardware):
    """
    GPIO MOTOR (GPIOMotor())
    Purpose: A template for controlling motors via Raspberry Pi GPIO pins.
    """
    def __init__(self, name, pin_pwm, pin_dir):
        super().__init__(name)
        self.pin_pwm = pin_pwm
        self.pin_dir = pin_dir
        self.velocity = 0.0

    def set_velocity(self, velocity):
        """
        In a real RPi, this would use RPi.GPIO to send a PWM signal.
        Here we log the physical instruction to the console.
        """
        self.velocity = velocity
        direction = "CLOCKWISE" if velocity >= 0 else "COUNTER-CLOCKWISE"
        # Simulate physical PWM duty cycle
        pwm_signal = min(abs(velocity) * 100, 100)
        
        # In professional logs, we record the physical pin action
        # print(f"[PHYSICAL] {self.name} -> Pin {self.pin_pwm} (PWM:{pwm_signal:.1f}%) | Pin {self.pin_dir} (DIR:{direction})")

    def stop(self):
        self.set_velocity(0.0)

class GenericSensor(BaseHardware):
    """
    GENERIC SENSOR (GenericSensor())
    Purpose: A template for reading physical sensors (I2C, SPI, etc.)
    """
    def __init__(self, name, address):
        super().__init__(name)
        self.address = address

    def read_value(self):
        """Reads data from the hardware address."""
        # This would interface with smbus or spidev in real life
        return 0.0
