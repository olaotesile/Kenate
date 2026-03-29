try:
    import RPi.GPIO as GPIO  # type: ignore
except Exception:
    GPIO = None

try:
    import smbus2  # type: ignore
except Exception:
    smbus2 = None

from .hal import BaseHardware


class RpiGpioMotor(BaseHardware):
    def __init__(self, name, pin_pwm, pin_dir, pwm_freq=1000):
        super().__init__(name)
        if GPIO is None:
            raise RuntimeError("RPi.GPIO is required for RpiGpioMotor")
        self.pin_pwm = pin_pwm
        self.pin_dir = pin_dir
        self.pwm_freq = pwm_freq
        self._pwm = None

    def connect(self):
        super().connect()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_pwm, GPIO.OUT)
        GPIO.setup(self.pin_dir, GPIO.OUT)
        self._pwm = GPIO.PWM(self.pin_pwm, self.pwm_freq)
        self._pwm.start(0)

    def disconnect(self):
        if self._pwm:
            self._pwm.stop()
        GPIO.cleanup()
        super().disconnect()

    def set_velocity(self, velocity):
        direction = GPIO.HIGH if velocity >= 0 else GPIO.LOW
        GPIO.output(self.pin_dir, direction)
        duty = min(abs(velocity) * 100, 100)
        if self._pwm:
            self._pwm.ChangeDutyCycle(duty)

    def stop(self):
        self.set_velocity(0.0)


class RpiI2CSensor(BaseHardware):
    def __init__(self, name, bus_id, address, reg=None):
        super().__init__(name)
        if smbus2 is None:
            raise RuntimeError("smbus2 is required for RpiI2CSensor")
        self.bus_id = bus_id
        self.address = address
        self.reg = reg
        self._bus = None

    def connect(self):
        super().connect()
        self._bus = smbus2.SMBus(self.bus_id)

    def disconnect(self):
        if self._bus:
            self._bus.close()
        super().disconnect()

    def read_value(self):
        if self._bus is None:
            raise RuntimeError("Sensor not connected")
        if self.reg is None:
            return self._bus.read_byte(self.address)
        return self._bus.read_byte_data(self.address, self.reg)


class TB6612Motor(BaseHardware):
    def __init__(self, name, pin_pwm, pin_in1, pin_in2, pwm_freq=1000):
        super().__init__(name)
        if GPIO is None:
            raise RuntimeError("RPi.GPIO is required for TB6612Motor")
        self.pin_pwm = pin_pwm
        self.pin_in1 = pin_in1
        self.pin_in2 = pin_in2
        self.pwm_freq = pwm_freq
        self._pwm = None

    def connect(self):
        super().connect()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_pwm, GPIO.OUT)
        GPIO.setup(self.pin_in1, GPIO.OUT)
        GPIO.setup(self.pin_in2, GPIO.OUT)
        self._pwm = GPIO.PWM(self.pin_pwm, self.pwm_freq)
        self._pwm.start(0)

    def disconnect(self):
        if self._pwm:
            self._pwm.stop()
        GPIO.cleanup()
        super().disconnect()

    def set_velocity(self, velocity):
        if velocity >= 0:
            GPIO.output(self.pin_in1, GPIO.HIGH)
            GPIO.output(self.pin_in2, GPIO.LOW)
        else:
            GPIO.output(self.pin_in1, GPIO.LOW)
            GPIO.output(self.pin_in2, GPIO.HIGH)
        duty = min(abs(velocity) * 100, 100)
        if self._pwm:
            self._pwm.ChangeDutyCycle(duty)

    def stop(self):
        self.set_velocity(0.0)


class L298NMotor(BaseHardware):
    def __init__(self, name, pin_enable, pin_in1, pin_in2, pwm_freq=1000):
        super().__init__(name)
        if GPIO is None:
            raise RuntimeError("RPi.GPIO is required for L298NMotor")
        self.pin_enable = pin_enable
        self.pin_in1 = pin_in1
        self.pin_in2 = pin_in2
        self.pwm_freq = pwm_freq
        self._pwm = None

    def connect(self):
        super().connect()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_enable, GPIO.OUT)
        GPIO.setup(self.pin_in1, GPIO.OUT)
        GPIO.setup(self.pin_in2, GPIO.OUT)
        self._pwm = GPIO.PWM(self.pin_enable, self.pwm_freq)
        self._pwm.start(0)

    def disconnect(self):
        if self._pwm:
            self._pwm.stop()
        GPIO.cleanup()
        super().disconnect()

    def set_velocity(self, velocity):
        if velocity >= 0:
            GPIO.output(self.pin_in1, GPIO.HIGH)
            GPIO.output(self.pin_in2, GPIO.LOW)
        else:
            GPIO.output(self.pin_in1, GPIO.LOW)
            GPIO.output(self.pin_in2, GPIO.HIGH)
        duty = min(abs(velocity) * 100, 100)
        if self._pwm:
            self._pwm.ChangeDutyCycle(duty)

    def stop(self):
        self.set_velocity(0.0)
