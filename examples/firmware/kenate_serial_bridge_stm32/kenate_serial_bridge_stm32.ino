/*
  Kenate Serial Bridge (STM32 / Arduino core)
  This sketch is compatible with STM32 boards that use the Arduino Core (e.g. STM32duino).

  Requires: ArduinoJson library.
*/

#include <ArduinoJson.h>

struct Motor {
  const char* name;
  float velocity;
  float position;
  float effort;
};

Motor motors[] = {
  {"left", 0.0, 0.0, 0.0},
  {"right", 0.0, 0.0, 0.0}
};

float readSensorByName(const char* name) {
  if (strcmp(name, "distance") == 0) return 42.0;
  if (strcmp(name, "battery") == 0) return 88.0;
  if (strcmp(name, "temp") == 0) return 35.0;
  return 0.0;
}

Motor* findMotor(const char* name) {
  for (size_t i = 0; i < sizeof(motors) / sizeof(motors[0]); i++) {
    if (strcmp(motors[i].name, name) == 0) return &motors[i];
  }
  return nullptr;
}

void respondOk(int id, float value = 0.0, bool includeValue = false) {
  StaticJsonDocument<128> resp;
  resp["id"] = id;
  resp["ok"] = true;
  if (includeValue) resp["value"] = value;
  serializeJson(resp, Serial);
  Serial.println();
}

void respondError(int id, const char* msg) {
  StaticJsonDocument<128> resp;
  resp["id"] = id;
  resp["ok"] = false;
  resp["error"] = msg;
  serializeJson(resp, Serial);
  Serial.println();
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (!Serial.available()) return;

  String line = Serial.readStringUntil('\n');
  if (line.length() == 0) return;

  StaticJsonDocument<256> doc;
  DeserializationError err = deserializeJson(doc, line);
  if (err) return;

  int id = doc["id"] | 0;
  const char* type = doc["type"] | "";

  if (strcmp(type, "motor_set") == 0) {
    const char* name = doc["name"] | "";
    const char* mode = doc["mode"] | "";
    float value = doc["value"] | 0.0;

    Motor* motor = findMotor(name);
    if (!motor) {
      respondError(id, "motor_not_found");
      return;
    }

    if (strcmp(mode, "velocity") == 0) motor->velocity = value;
    else if (strcmp(mode, "position") == 0) motor->position = value;
    else if (strcmp(mode, "effort") == 0) motor->effort = value;
    else {
      respondError(id, "invalid_mode");
      return;
    }

    respondOk(id);
    return;
  }

  if (strcmp(type, "sensor_get") == 0) {
    const char* name = doc["name"] | "";
    float value = readSensorByName(name);
    respondOk(id, value, true);
    return;
  }

  respondError(id, "unknown_type");
}
