#include <iostream>

class PIDController {
private:
    double kp, ki, kd;
    double prev_error;
    double integral;

public:
    PIDController(double p = 1.0, double i = 0.0, double d = 0.1) 
        : kp(p), ki(i), kd(d), prev_error(0.0), integral(0.0) {}

    double compute(double setpoint, double current_value, double dt) {
        if (dt <= 0.0) return 0.0;
        double error = setpoint - current_value;
        integral += error * dt;
        double derivative = (error - prev_error) / dt;
        prev_error = error;
        return (kp * error) + (ki * integral) + (kd * derivative);
    }

    void reset() {
        prev_error = 0.0;
        integral = 0.0;
    }
};
