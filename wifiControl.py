import os
import time
import ipaddress
import wifi
import socketpool
import board
import microcontroller
import digitalio
import pwmio
from adafruit_motor import motor
from digitalio import DigitalInOut, Direction
from adafruit_httpserver import Server, Request, Response, POST


class Robot:
    """Encapsulates robot motor control."""
    
    def __init__(self):
        """Initialize motors and set default speed."""
        # Left Motor
        pwm_1a = pwmio.PWMOut(board.GP8, frequency=10000)
        pwm_1b = pwmio.PWMOut(board.GP9, frequency=10000)
        self.motor_left = motor.DCMotor(pwm_1a, pwm_1b)
        
        # Right Motor
        pwm_2a = pwmio.PWMOut(board.GP10, frequency=10000)
        pwm_2b = pwmio.PWMOut(board.GP11, frequency=10000)
        self.motor_right = motor.DCMotor(pwm_2a, pwm_2b)
        
        self.speed = 0.5
    
    def move(self, left_throttle, right_throttle):
        """Apply throttle to both motors."""
        self.motor_left.throttle = left_throttle
        self.motor_right.throttle = right_throttle
    
    def move_forward(self):
        """Move forward."""
        print("Forward")
        self.move(self.speed, self.speed+0.03)  # Slightly faster on right for straight movement
    
    def move_backward(self):
        """Move backward."""
        print("Backward")
        self.move(-self.speed, -self.speed-0.03)
    
    def move_left(self):
        """Move left."""
        print("Left")
        self.move(0, self.speed)
    
    def move_right(self):
        """Move right."""
        print("Right")
        self.move(self.speed, 0)
    
    def turn_left(self):
        """Turn left in place."""
        print("Turn Left")
        self.move(-self.speed, self.speed)
    
    def turn_right(self):
        """Turn right in place."""
        print("Turn Right")
        self.move(self.speed, -self.speed)
    
    def move_stop(self):
        """Stop all movement."""
        print("Stop")
        self.move(0, 0)
    
    def set_speed(self, new_speed):
        """Set the movement speed (0-1)."""
        self.speed = max(-0.95, min(0.95, new_speed))
        print(f"Speed set to {self.speed}")
    
    def get_speed(self):
        """Get the current speed."""
        return self.speed


class RobotServer:
    """Encapsulates the HTTP server for robot control."""
    
    def __init__(self, robot, ip_address):
        """Initialize the server with a robot instance."""
        self.robot = robot
        self.ip_address = ip_address
        
        pool = socketpool.SocketPool(wifi.radio)
        self.server = Server(pool, "/static", debug=False)
        self.html_content = None
        
        # Load HTML content once at startup
        try:
            with open("/static/index.html", "r") as f:
                self.html_content = f.read()
        except Exception as e:
            print(f"Error loading index.html: {e}")
            self.html_content = "<h1>Error loading page</h1>"
        
        # Register routes
        @self.server.route("/")
        def base(request: Request):
            return Response(request, self.html_content, content_type='text/html')

        @self.server.route("/", POST)
        def buttonpress(request: Request):
            return self.handle_command(request)
    
    def handle_command(self, request: Request):
        """Process incoming HTTP commands."""
        raw_text = request.body.decode("utf8")
        
        print(f"{raw_text=}")
        if "forward" in raw_text:
            self.robot.move_forward()
        elif "backward" in raw_text:
            self.robot.move_backward()
        elif "turn_right" in raw_text:
            self.robot.turn_right()
        elif "turn_left" in raw_text:
            self.robot.turn_left()
        elif "right" in raw_text:
            self.robot.move_right()
        elif "left" in raw_text:
            self.robot.move_left()
        elif "speed=" in raw_text:
            # Extract speed value from request
            try:
                speed_str = raw_text.split("speed=")[1]
                speed = float(speed_str)
                self.robot.set_speed(speed)
            except Exception as e:
                print(f"Invalid speed value: {e}")
        elif "stop" in raw_text:
            self.robot.move_stop()
            
        return Response(request, self.html_content, content_type='text/html')
    
    def start(self):
        """Start the HTTP server."""
        print("Starting server...")
        self.server.start(str(self.ip_address), port=80)
        print(f"Server running at http://{self.ip_address}")
    
    def run(self):
        """Main server loop."""
        while True:
            self.server.poll()


def main():
    """Main entry point."""
    # Connect to network
    try:
        wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
        print("Connected. IP:", wifi.radio.ipv4_address)
    except Exception as e:
        print("WiFi connect error:", str(e))
        # stop the program from trying to start the server without a connection
        raise SystemExit
    
    # Create robot and server
    robot = Robot()
    server = RobotServer(robot, wifi.radio.ipv4_address)
    
    # Start the server
    server.start()
    server.run()


if __name__ == "__main__":
    main()