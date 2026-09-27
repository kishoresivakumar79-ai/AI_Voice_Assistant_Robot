# AI Voice Assistant Robot — Hardware Architecture & Connection Specs

This document defines the physical hardware component wiring, power routing, and pin mappings.

---

## Hardware Component Specifications

| Hardware Component | Category | Function / Operational Spec |
| :--- | :--- | :--- |
| **Raspberry Pi 5 (8GB)** | Single Board Computer | Main AI Engine, ROS2 Node host, Whisper STT & Vision Processing |
| **ESP32 DevKit V1** | Microcontroller | Low-level PWM Motor Driver, Encoder pulse counter & IMU reader |
| **L298N Dual H-Bridge** | Motor Controller | Drives dual DC Motors up to 2A per channel with PWM speed control |
| **USB Microphone** | Audio Input | Clean noise-canceling voice capture for wake word detection |
| **MAX98357A I2S Amp + Speaker** | Audio Output | 3W Class-D amplifier for robot voice feedback |
| **Raspberry Pi Camera V2/V3** | Vision Sensor | CSI camera interface delivering 1080p face tracking feed |
| **MPU6050 (I2C)** | IMU | 6-DOF Accelerometer + Gyroscope for robot balance & odometry |
| **HC-SR04 Ultrasonic** | Rangefinder | Front/rear distance sensors for obstacle collision avoidance |
| **LiDAR (RPLIDAR A1/A2)** | Spatial Mapping | 360-degree laser scanner for ROS2 SLAM and Navigation |
| **12V Li-Ion Battery + BMS** | Power Supply | High discharge power for motors + 5V 5A step-down buck converter for Pi5 |

---

## Pinout & Wiring Diagram

```
[ Raspberry Pi 5 ] 
   │
   ├─► USB 3.0 ───────► USB Microphone (Audio In)
   ├─► USB 2.0 ───────► RPLIDAR A1 (LiDAR USB Serial)
   ├─► CSI Ribbon ────► Pi Camera V3 (Vision)
   ├─► GPIO 18, 19, 21─► MAX98357A Amp (I2S Audio Out: BCLK, LRC, DIN)
   └─► USB Serial ────► ESP32 Microcontroller (ROS2 Serial / Micro-ROS)

[ ESP32 DevKit ] ───► L298N Motor Driver Interface:
   ├─► GPIO 26 (ENA) ──► L298N Enable A (PWM Left Speed)
   ├─► GPIO 27 (IN1) ──► L298N IN1 (Left Forward)
   ├─► GPIO 14 (IN2) ──► L298N IN2 (Left Reverse)
   ├─► GPIO 12 (IN3) ──► L298N IN3 (Right Forward)
   ├─► GPIO 13 (IN4) ──► L298N IN4 (Right Reverse)
   ├─► GPIO 25 (ENB) ──► L298N Enable B (PWM Right Speed)
   │
   ├─► GPIO 34, 35 ───► Left Quadrature Encoder (Phase A, B)
   ├─► GPIO 32, 33 ───► Right Quadrature Encoder (Phase A, B)
   │
   ├─► GPIO 21 (SDA) ──► MPU6050 IMU SDA
   └─► GPIO 22 (SCL) ──► MPU6050 IMU SCL
```

---

## Power Routing

```
[ 12V Li-Ion Battery (3S Pack) ]
   │
   ├─► [ Power Switch ] ──► [ L298N Motor Power Terminals (12V Input) ]
   │
   └─► [ 12V-to-5V 5A Buck Converter ] ──► Type-C 5V Input to Raspberry Pi 5
```
