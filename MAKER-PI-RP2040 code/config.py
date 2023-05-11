import board
import digitalio
import neopixel
import pwmio
import simpleio
from adafruit_motor import motor

from sensor import Sensor

# Initialize buttons
btn1 = digitalio.DigitalInOut(board.GP20)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP
btn2 = digitalio.DigitalInOut(board.GP21)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.UP

# Initialize DC motors
m1a = pwmio.PWMOut(board.GP8, frequency=10000)
m1b = pwmio.PWMOut(board.GP9, frequency=10000)
m2a = pwmio.PWMOut(board.GP10, frequency=10000)
m2b = pwmio.PWMOut(board.GP11, frequency=10000)
motor_r = motor.DCMotor(m1a, m1b)
motor_l = motor.DCMotor(m2b, m2a)

# Initialize Analog IR Sensors
ir_right = Sensor(board.GP27)
ir_mid = Sensor(board.GP26)
ir_left = Sensor(board.GP28)

# Initialize Neopixel RGB LEDs
pixels = neopixel.NeoPixel(board.GP18, 2)
pixels.fill(0)

# Define pin connected to piezo buzzer
PIEZO_PIN = board.GP22


# Configure tunes
def start_tune():
    simpleio.tone(PIEZO_PIN, 262, duration=0.1)
    simpleio.tone(PIEZO_PIN, 659, duration=0.15)
    simpleio.tone(PIEZO_PIN, 784, duration=0.2)


def stop_tune():
    simpleio.tone(PIEZO_PIN, 784, duration=0.1)
    simpleio.tone(PIEZO_PIN, 659, duration=0.15)
    simpleio.tone(PIEZO_PIN, 262, duration=0.2)


# Initialize Remote Control Inputs
m_l_forward = digitalio.DigitalInOut(board.GP17)
m_l_backward = digitalio.DigitalInOut(board.GP2)
m_r_forward = digitalio.DigitalInOut(board.GP7)
m_r_backward = digitalio.DigitalInOut(board.GP3)

m_l_forward.direction = digitalio.Direction.INPUT
m_l_backward.direction = digitalio.Direction.INPUT
m_r_forward.direction = digitalio.Direction.INPUT
m_r_backward.direction = digitalio.Direction.INPUT
