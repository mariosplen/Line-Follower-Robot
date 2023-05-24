import time

import behaviors
from config import (
    btn1,
    btn2,
    ir_left,
    ir_mid,
    ir_right,
    start_tune,
    stop_tune,
    motor_r,
    motor_l,
    m_l_forward,
    m_l_backward,
    m_r_forward,
    m_r_backward,
    # uart, write_info,
)

# State codes represented as binary constants where each digit corresponds to a sensor detecting a black line.
# Example: 010 means the middle sensor detecting a line.
COAST = 0b000
RIGHT_TURN = 0b001
LINE_FOLLOW1 = 0b010
LINE_FOLLOW2 = 0b011
LEFT_TURN = 0b100
UNREACHABLE_STOP = 0b101
LINE_FOLLOW3 = 0b110
STOP = 0b111

# Map each state code to the appropriate behavior function
states = {
    COAST: behaviors.coast,
    RIGHT_TURN: behaviors.right_turn,
    LINE_FOLLOW1: behaviors.line_follow,
    LINE_FOLLOW2: behaviors.line_follow,
    LEFT_TURN: behaviors.left_turn,
    UNREACHABLE_STOP: behaviors.stop,
    LINE_FOLLOW3: behaviors.line_follow,
    STOP: behaviors.stop,
}


def follow(max_speed):
    behaviors.speed = max_speed
    start_tune()
    while True:
        sensor_data = (ir_left.is_above_line(), ir_mid.is_above_line(), ir_right.is_above_line())
        # Convert the boolean sensor readings for left, middle, and right IR sensors to an integer state.
        # Each sensor reading represents a binary digit, so we can represent all possible sensor combinations
        # with a unique integer from 0 to 7. For example, (False, False, False) becomes 0, (False, False,
        # True) becomes 1, (False, True, False) becomes 2, and so on.
        state = (int(sensor_data[0]) << 2) | (int(sensor_data[1]) << 1) | int(sensor_data[2])
        # Call the function associated with the current state
        states[state]()
        if state == STOP:
            stop_tune()
            # print("Finished!")
            break


# DISABLED BECAUSE UNSTABLE
# def read_info():
#     global speed
#     data = uart.read(5)  # Read up to 5 bytes
#
#     if data is not None:
#         data_string = data.decode('utf-8')  # Convert bytes to string
#
#         if "CALBR" in data_string:
#             behaviors.calibrate()
#         elif "FOLLO" in data_string:
#             behaviors.follow(behaviors.speed)
#         elif "S," in data_string:
#             print(data_string)
#             # Extract the speed state number from the received data
#             speed_state = int(data_string.split(",")[1])
#             behaviors.speed = speed_state / 100


def main():
    # Define the interval in seconds for the DHT reading
    # interval = 10

    # Start time
    # start_time = time.monotonic()

    while True:

        # Check if the interval has passed
        # current_time = time.monotonic()
        # if current_time - start_time >= interval:
        #     # Call the function
        #     read_info()
        #     write_info()
        #     # Update the start time
        #     start_time = current_time

        # Code for the RC
        motor_l_value = 0
        motor_r_value = 0
        if m_l_forward.value:
            motor_l_value = behaviors.speed
        elif m_l_backward.value:
            motor_l_value = -1 * behaviors.speed
        if m_r_forward.value:
            motor_r_value = behaviors.speed
        elif m_r_backward.value:
            motor_r_value = -1 * behaviors.speed

        motor_l.throttle = motor_l_value
        motor_r.throttle = motor_r_value

        # The robot can be powered by either 4xAA batteries or a rechargeable Lipo. To enable maximum speed,
        # press btn2 when using 4xAA batteries, and btn1 when using the Lipo. If both buttons are pressed
        # simultaneously for at least 1 second, the calibration process will start.
        if not btn1.value:
            start_time = time.time()
            while True:
                if not btn2.value:
                    # print("Calibration started")
                    behaviors.calibrate()
                    break
                if time.time() - start_time > 2:
                    # print("btn1 pressed")
                    follow(0.5)
                    break
        if not btn2.value:
            start_time = time.time()
            while True:
                if not btn1.value:
                    # print("Calibration started")
                    behaviors.calibrate()
                    break
                    # print("Calibration finished!")
                if time.time() - start_time > 1:
                    # print("btn2 pressed")
                    follow(1)
                    break


if __name__ == "__main__":
    main()
