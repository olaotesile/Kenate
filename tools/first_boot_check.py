import argparse
import time

from kenate.hal_serial import SerialTransport, SerialMotor, SerialSensor


def main():
    parser = argparse.ArgumentParser(description="Kenate First-Boot Hardware Check")
    parser.add_argument("--port", required=True, help="Serial port (COM3 or /dev/ttyUSB0)")
    parser.add_argument("--baudrate", type=int, default=115200)
    args = parser.parse_args()

    transport = SerialTransport(port=args.port, baudrate=args.baudrate, timeout=0.5)
    left = SerialMotor(transport, "left")
    right = SerialMotor(transport, "right")
    distance = SerialSensor(transport, "distance")

    print("[CHECK] Reading sensor...")
    value = distance.read_value()
    print(f"[OK] Distance sensor value: {value}")

    print("[CHECK] Spinning left motor for 1s...")
    left.set_velocity(0.3)
    time.sleep(1.0)
    left.stop()
    print("[OK] Left motor stop")

    print("[CHECK] Spinning right motor for 1s...")
    right.set_velocity(0.3)
    time.sleep(1.0)
    right.stop()
    print("[OK] Right motor stop")

    transport.close()
    print("[DONE] First-boot check complete.")


if __name__ == "__main__":
    main()
