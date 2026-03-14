'''
Obstacle Avoidance Robot using 3V-5.5V SR04P Ultrasonic Ranging Module.
Additional Library:
    - adafruit_hcsr04.mpy
    - adafruit_motor
'''

import time
import board
import digitalio
import pwmio

from wifiControl import main as wifi_main
from obstacleAvoidance import main as obstacle_main

# Button Setup
gp21 = digitalio.DigitalInOut(board.GP21)
gp21.direction = digitalio.Direction.INPUT
gp21.pull = digitalio.Pull.UP

gp20 = digitalio.DigitalInOut(board.GP20)
gp20.direction = digitalio.Direction.INPUT
gp20.pull = digitalio.Pull.UP


''' Main entry point for the robot. Waits for button presses to set the mission mode.'''

print("="*20)
print("Welcome the Robo Pico Control Car!")
print("Press GP21 button to start wifi control mode...")
print("Press GP20 button to start obstacle avoidance mode...")
print("="*20)
print()
print("Waiting for button press...")
while True:
    # run the server
    if not gp21.value:  # Button pressed (active low)
        print("Button pressed! Starting obstacle avoidance robot...")
        wifi_main()
    
    elif not gp20.value:  # Button pressed (active low)
        print("Button pressed! Starting obstacle avoidance robot...")
        obstacle_main()