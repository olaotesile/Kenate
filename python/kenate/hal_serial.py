import json
import threading
import time

try:
    import serial  # type: ignore
except Exception:
    serial = None

from .hal import BaseHardware


class SerialTransport:
    def __init__(self, port, baudrate=115200, timeout=0.5):
        if serial is None:
            raise RuntimeError(
                "pyserial is required for SerialTransport. Install with: pip install pyserial"
            )
        self._ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self._lock = threading.Lock()
        self._next_id = 1

    def close(self):
        if self._ser:
            self._ser.close()

    def _read_line(self):
        line = self._ser.readline()
        if not line:
            return None
        try:
            return line.decode("utf-8").strip()
        except Exception:
            return None

    def request(self, payload, timeout=1.0):
        with self._lock:
            req_id = self._next_id
            self._next_id += 1
            payload["id"] = req_id
            data = (json.dumps(payload) + "\n").encode("utf-8")
            self._ser.write(data)

            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                line = self._read_line()
                if not line:
                    continue
                try:
                    resp = json.loads(line)
                except Exception:
                    continue
                if resp.get("id") == req_id:
                    return resp
        return {"id": req_id, "ok": False, "error": "timeout"}


class SerialMotor(BaseHardware):
    def __init__(self, transport, name):
        super().__init__(name)
        self._transport = transport

    def set_velocity(self, velocity):
        return self._transport.request(
            {"type": "motor_set", "name": self.name, "mode": "velocity", "value": velocity}
        )

    def set_position(self, position):
        return self._transport.request(
            {"type": "motor_set", "name": self.name, "mode": "position", "value": position}
        )

    def set_effort(self, effort):
        return self._transport.request(
            {"type": "motor_set", "name": self.name, "mode": "effort", "value": effort}
        )

    def stop(self):
        return self.set_velocity(0.0)


class SerialSensor(BaseHardware):
    def __init__(self, transport, name):
        super().__init__(name)
        self._transport = transport

    def read_value(self):
        resp = self._transport.request({"type": "sensor_get", "name": self.name})
        if resp.get("ok"):
            return resp.get("value")
        return None
