"""
Obstacle Avoidance Robot using 3V-5.5V SR04P Ultrasonic Ranging Module.
Additional Library:
    - adafruit_hcsr04.mpy
    - adafruit_motor
"""

import time
import board
import digitalio
import pwmio
from adafruit_motor import motor
import adafruit_hcsr04


class ObstacleAvoidanceRobot:
    """Encapsulates obstacle avoidance robot behavior."""
    
    def __init__(self):
        """Initialize motors, sonar sensor, and button."""
        # Ultrasonic Sensor Setup
        self.sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP16, echo_pin=board.GP17)
        
        # Left Motor
        pwm_1a = pwmio.PWMOut(board.GP8, frequency=10000)
        pwm_1b = pwmio.PWMOut(board.GP9, frequency=10000)
        self.motor_left = motor.DCMotor(pwm_1a, pwm_1b)
        
        # Right Motor
        pwm_2a = pwmio.PWMOut(board.GP10, frequency=10000)
        pwm_2b = pwmio.PWMOut(board.GP11, frequency=10000)
        self.motor_right = motor.DCMotor(pwm_2a, pwm_2b)
        
        self.running = False
    
    def move(self, left_throttle, right_throttle):
        """Apply throttle to both motors."""
        self.motor_left.throttle = left_throttle
        self.motor_right.throttle = right_throttle
    
    def read_distance(self):
        """Read distance from ultrasonic sensor."""
        time.sleep(0.1)
        return self.sonar.distance
    
    def avoid_obstacle(self):
        """Main obstacle avoidance loop."""
        print("Obstacle avoidance mode active...")
        self.running = True
        
        while self.running:
            try:
                distance = self.read_distance()
                print(f"Distance: {distance} cm")
                
                if distance < 10:  # Obstacle detected
                    print("Obstacle detected! Turning left...")
                    self.move(0.1, 0.5)  # Turn Left
                    time.sleep(1)
                else:  # No obstacle
                    self.move(0.5, 0.54)  # Move Forward
                    
            except RuntimeError:
                print("Ultrasonic sensor error. Retrying...")
                self.move(0, 0)  # Stop in case of sensor error
                time.sleep(0.1)
    
    def stop(self):
        """Stop the robot and exit obstacle avoidance mode."""
        print("Stopping obstacle avoidance mode...")
        self.running = False
        self.move(0, 0)


def main():
    """Main entry point for obstacle avoidance robot."""
    robot = ObstacleAvoidanceRobot()
    
    while True:
            print("Starting obstacle avoidance robot...")
            robot.avoid_obstacle()
            time.sleep(0.5)  # Debounce delay


if __name__ == "__main__":
    main()