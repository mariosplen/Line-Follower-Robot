import time

from config import (
    motor_l,
    motor_r,
    ir_left,
    ir_mid,
    ir_right
)

# Setup variables for PID algorithm
P, D, I, previous_error, PID_value, error = 0, 0, 0, 0, 0, 0
lsp, rsp = 0, 0

# Speed variable
speed = 1

# PID constants
Kp = 0.2
Kd = 4.5
Ki = 0


# Define functions for each behavior

# Calibrate sensors

def calibrate():
    time.sleep(1)
    calibrate_internal()
    time.sleep(0.5)
    calibrate_internal(clockwise=False)


def calibrate_internal(clockwise=True):
    min_values = [3.3, 3.3, 3.3]
    max_values = [0, 0, 0]
    thresholds = [1.65, 1.65, 1.65]
    if clockwise:
        motor_l.throttle = 0.5
        motor_r.throttle = -0.5
    else:
        motor_l.throttle = -0.5
        motor_r.throttle = 0.5
    for i in range(9000):
        sensor_values = [ir_left.value(), ir_mid.value(), ir_right.value()]
        for j in range(3):
            if sensor_values[j] < min_values[j]:
                min_values[j] = sensor_values[j]
            if sensor_values[j] > max_values[j]:
                max_values[j] = sensor_values[j]
    for i in range(3):
        thresholds[i] = (min_values[i] + max_values[i]) / 2

    sensors = [(ir_left, min_values[0], max_values[0], thresholds[0]),
               (ir_mid, min_values[1], max_values[1], thresholds[1]),
               (ir_right, min_values[2], max_values[2], thresholds[2])
               ]

    for sensor, min_val, max_val, threshold in sensors:
        sensor.set_min(min_val)
        sensor.set_max(max_val)
        sensor.set_threshold(threshold)

    motor_l.throttle = 0
    motor_r.throttle = 0


# PID algorithm implementation for line following
def line_follow():
    global Kp, Kd, Ki
    global P, D, I, previous_error, PID_value, error
    global speed
    global lsp, rsp
    error = ir_left.value() - ir_right.value()
    P = error
    I = I + error
    D = error - previous_error

    PID_value = (Kp * P) + (Ki * I) + (Kd * D)
    previous_error = error

    lsp = speed - PID_value
    rsp = speed + PID_value

    # Make sure the speeds are within bounds, the motors work only on the speeds between 0.5 and speed variable
    lsp = max(0.0, min(speed, lsp))
    rsp = max(0.0, min(speed, rsp))

    # Set motor speeds
    motor_l.throttle = lsp
    motor_r.throttle = rsp


def stop():
    global lsp, rsp
    lsp = 0
    rsp = 0
    motor_l.throttle = 0
    motor_r.throttle = 0


def left_turn():
    global lsp, rsp
    lsp = 0
    rsp = speed
    motor_l.throttle = 0
    motor_r.throttle = speed


def right_turn():
    global lsp, rsp
    lsp = speed
    rsp = 0
    motor_l.throttle = speed
    motor_r.throttle = 0


# The robot is coasting when it has lost the way, so the turns should be sharp
def coast():
    global lsp, rsp
    if lsp > rsp:
        right_turn()
    else:
        left_turn()
