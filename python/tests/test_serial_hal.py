from kenate.hal_serial import SerialMotor, SerialSensor


class DummyTransport:
    def __init__(self):
        self.last_payload = None
        self.responses = []
        self.next_id = 1

    def request(self, payload, timeout=1.0):
        self.last_payload = payload
        return self.responses.pop(0) if self.responses else {"ok": True, "id": self.next_id}


def test_serial_motor_payload():
    transport = DummyTransport()
    motor = SerialMotor(transport, "left")
    motor.set_velocity(0.5)
    assert transport.last_payload["type"] == "motor_set"
    assert transport.last_payload["name"] == "left"
    assert transport.last_payload["mode"] == "velocity"
    assert transport.last_payload["value"] == 0.5


def test_serial_sensor_payload_and_response():
    transport = DummyTransport()
    transport.responses.append({"ok": True, "id": 1, "value": 12.3})
    sensor = SerialSensor(transport, "distance")
    value = sensor.read_value()
    assert transport.last_payload["type"] == "sensor_get"
    assert value == 12.3
