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

SPEED = 0.5

# Left Motor
PWM_M1A = board.GP8
PWM_M1B = board.GP9
# Right Motor
PWM_M2A = board.GP10
PWM_M2B = board.GP11

# DC motor setup
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=10000)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=10000)
motorL = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=10000)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=10000)
motorR = motor.DCMotor(pwm_2a, pwm_2b)

def move(sL, sR):
    """Aplica la velocidad a ambos motores."""
    motorL.throttle = sL
    motorR.throttle = sR

def move_forward():
    print("Forward")
    move(SPEED, SPEED)
    
def move_backward():
    print("Backward")
    move(-SPEED, -SPEED)
    
def move_left():
    print("Left")
    move(0, SPEED)
    
def move_right():
    print("Right")
    move(SPEED, 0)

def turn_left():
    print("Turn Left")
    move(-SPEED, SPEED)

def turn_right():
    print("Turn Right")
    move(SPEED, -SPEED)
    
def move_stop():
    print("Stop")
    move(0, 0) 

def set_speed(new_speed):
    global SPEED
    SPEED = new_speed
    print(f"Speed set to {SPEED}")

# Connect to network
try:
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    print("Connected. IP:", wifi.radio.ipv4_address)
except Exception as e:
    print("WiFi connect error:", str(e))
    # stop the program from trying to start the server without a connection
    raise SystemExit 

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=False)

def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Robo Pico Control</title>
    <script>
    function buttonDown(button) {{
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(button + "=true");
    }}
    function buttonUp() {{
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("stop=true");
    }}
    function setSpeed(value) {{
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("speed=" + value);
        document.getElementById("speedValue").textContent = Math.round(value * 100) + "%";
    }}
    </script>
    <style>
      h1 {{
        text-align: center;
      }}
      body {{
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 80vh;
          margin: 0;
      }}
      .controls {{
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 10px;
      }}
      .button {{
          font-size: 90px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: white;
          padding: 10px;
          user-select: none;
          width: 80px;
          height: 80px;
      }}
      .slider-container {{
          margin-top: 30px;
          text-align: center;
      }}
      .slider {{
          width: 200px;
          height: 8px;
          margin: 10px 0;
      }}
    </style>
    </head>
    <body>
    <h1>Robo Pico Wifi Control Car</h1>
    <div class="controls">
        <div></div>
        <div class="button" id="forward" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬆️</div>
        <div></div>
        
        <div class="button" id="turn_left" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">↩️</div>
        <div></div>
        <div class="button" id="turn_right" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">↪️</div>
        
        <div class="button" id="left" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬅️</div>
        <div></div>
        <div class="button" id="right" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">➡️</div>
        
        <div></div>
        <div class="button" id="backward" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬇️</div>
        <div></div>
    </div>
    <div class="slider-container">
        <label for="speedSlider">Speed:</label>
        <br>
        <input type="range" id="speedSlider" class="slider" min="0" max="1" step="0.01" value="0.5" oninput="setSpeed(this.value)">
        <br>
        <span id="speedValue">50%</span>
    </div>
    </body>
    </html>
    """
    return html

@server.route("/")
def base(request: Request):
    return Response(request, webpage(), content_type='text/html')

@server.route("/", POST)
def buttonpress(request: Request):
    raw_text = request.body.decode("utf8")
    
    print(f"{raw_text=}")
    if "forward" in raw_text:
        move_forward()
    elif "backward" in raw_text:
        move_backward()
    elif "turn_right" in raw_text:
        turn_right()
    elif "turn_left" in raw_text:
        turn_left()
    elif "right" in raw_text:
        move_right()
    elif "left" in raw_text:
        move_left()
    elif "speed=" in raw_text:
        # Extract speed value from request
        speed_str = raw_text.split("speed=")[1]
        try:
            speed = max(-1, min(1, float(speed_str)))
            set_speed(speed)
        except:
            print("Invalid speed value")
    elif "stop" in raw_text:
        move_stop()
        
    return Response(request, webpage(), content_type='text/html')

print("Starting server...")
server.start(str(wifi.radio.ipv4_address), port=80)
print(f"Server running at http://{wifi.radio.ipv4_address}")

while True:
    server.poll()