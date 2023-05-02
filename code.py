import time

import behaviors
from config import start_btn, calibrate_btn, ir_left, ir_mid, ir_right, start_tune, stop_tune

# Define the behavior codes as binary constants
COAST = 0b000
RIGHT_TURN = 0b001
LINE_FOLLOW1 = 0b010
LINE_FOLLOW2 = 0b011
LEFT_TURN = 0b100
UNREACHABLE_STOP = 0b101
LINE_FOLLOW3 = 0b110
STOP = 0b111


def main():
    # Define a dictionary that maps state codes to functions
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

    while True:
        if not calibrate_btn.value:
            time.sleep(1)
            behaviors.calibrate()
            time.sleep(0.5)
            behaviors.calibrate(clockwise=False)
        if not start_btn.value:
            start_tune()
            while True:
                sensor_data = (ir_left.is_above_line(), ir_mid.is_above_line(), ir_right.is_above_line())
                state = (int(sensor_data[0]) << 2) | (int(sensor_data[1]) << 1) | int(sensor_data[2])
                states[state]()
                if state == STOP:
                    stop_tune()
                    break


if __name__ == "__main__":
    main()
