/*
 * AI Voice Assistant Robot - ESP32 Motor Controller Firmware
 * Board: ESP32 Dev Module
 */

#define ENA_PIN 26
#define IN1_PIN 27
#define IN2_PIN 14
#define IN3_PIN 12
#define IN4_PIN 13
#define ENB_PIN 25

// PWM Setup
const int PWM_FREQ = 5000;
const int PWM_RES = 8; // 0-255 range

void setup() {
  Serial.begin(115200);
  
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);

  // Configure ESP32 LEDC PWM channels
  ledcAttach(ENA_PIN, PWM_FREQ, PWM_RES);
  ledcAttach(ENB_PIN, PWM_FREQ, PWM_RES);

  stopMotors();
  Serial.println("[ESP32] Motor Controller Firmware Ready.");
}

void setMotorSpeeds(int leftPWM, int rightPWM) {
  // Left Motor Direction
  if (leftPWM > 0) {
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
  } else if (leftPWM < 0) {
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, HIGH);
  } else {
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, LOW);
  }

  // Right Motor Direction
  if (rightPWM > 0) {
    digitalWrite(IN3_PIN, HIGH);
    digitalWrite(IN4_PIN, LOW);
  } else if (rightPWM < 0) {
    digitalWrite(IN3_PIN, LOW);
    digitalWrite(IN4_PIN, HIGH);
  } else {
    digitalWrite(IN3_PIN, LOW);
    digitalWrite(IN4_PIN, LOW);
  }

  ledcWrite(ENA_PIN, abs(leftPWM));
  ledcWrite(ENB_PIN, abs(rightPWM));
}

void stopMotors() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  ledcWrite(ENA_PIN, 0);
  ledcWrite(ENB_PIN, 0);
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.startsWith("CMD")) {
      // Format: CMD,<leftPWM>,<rightPWM>
      int comma1 = cmd.indexOf(',');
      int comma2 = cmd.indexOf(',', comma1 + 1);
      if (comma1 > 0 && comma2 > 0) {
        int left = cmd.substring(comma1 + 1, comma2).toInt();
        int right = cmd.substring(comma2 + 1).toInt();
        setMotorSpeeds(left, right);
        Serial.printf("[ESP32 OK] Left: %d, Right: %d\n", left, right);
      }
    } else if (cmd == "STOP") {
      stopMotors();
      Serial.println("[ESP32 OK] Motors Stopped.");
    }
  }
}
