from config import motor_l, motor_r, ir_left, ir_mid, ir_right

# Setup variables for PID algorithm
P, D, I, previous_error, PID_value, error = 0, 0, 0, 0, 0, 0
lsp, rsp = 0, 0

lf_speed = 0.8
Kp = 0.1
Kd = 0.1
Ki = 0


# Define functions for each behavior

def calibrate(clockwise=True):
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


def follow_line():
    global Kp, Kd, Ki
    global P, D, I, previous_error, PID_value, error
    global lf_speed
    global lsp, rsp
    error = ir_left.value() - ir_right.value()
    P = error
    I = I + error
    D = error - previous_error

    PID_value = (Kp * P) + (Ki * I) + (Kd * D)
    previous_error = error

    lsp = lf_speed - PID_value
    rsp = lf_speed + PID_value

    # Make sure the speeds are within bounds, the motors work only on the speeds between 0.5 and 1.0
    lsp = max(0.0, min(1.0, lsp))
    rsp = max(0.0, min(1.0, rsp))

    # Set motor speeds
    motor_l.throttle = lsp
    motor_r.throttle = rsp


def stop():
    global lsp, rsp
    lsp = 0
    rsp = 0
    motor_l.throttle = 0
    motor_r.throttle = 0
    # Play tones


def line_follow():
    # global Kp, Kd, Ki
    # Kp = ...
    # Kd = ...
    # Ki = ...
    follow_line()


def left_turn():
    global lsp, rsp
    lsp = 0
    rsp = lf_speed
    motor_l.throttle = 0
    motor_r.throttle = lf_speed


def right_turn():
    global lsp, rsp
    lsp = lf_speed
    rsp = 0
    motor_l.throttle = lf_speed
    motor_r.throttle = 0


def coast():
    global lsp, rsp
    if lsp > rsp:
        right_turn()
    else:
        left_turn()
