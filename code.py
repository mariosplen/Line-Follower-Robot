import time

import behaviors
from config import start_btn, calibrate_btn, ir_left, ir_mid, ir_right, start_tune, stop_tune

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


def main():
    while True:
        if not calibrate_btn.value:
            # print("Calibration button pressed")
            time.sleep(1)
            behaviors.calibrate()
            time.sleep(0.5)
            behaviors.calibrate(clockwise=False)
            # print("Calibration finished!")
        if not start_btn.value:
            # print("Start button pressed")
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


if __name__ == "__main__":
    main()
