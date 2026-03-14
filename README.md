# Bocobot Code Repository

This repo contains code for [Cytron's Bocobot](https://www.cytron.io/p-bocobot-robotic-kits-for-raspberry-pi-pico-pico-w), a small robot designed for educational purposes and for learning mobile and behaviour-based robotics. The code is written in CircuitPython and runs on a Raspberry Pi Pico W microcontroller.

<img src="https://static.cytron.io/image/cache/catalog/products/KIT-ROBO-PICO/v-bocobot-1-800x800.jpg" alt="Bocobot" width="300"/>

The robot has the following features:
- Special PCB for connecting all components, with leds, buttons, and a buzzer
- WiFi connectivity for remote control and monitoring
- Two TT motors for movement
- An ultrasonic sensor for obstacle detection (HC-SR04)
- A light sensor (photoresistor) for ambient light detection
- A line follower sensor for line tracking with an array of 5 IR sensors.
- Battery powered trough 4 1.5V AA batteries.

## Getting Started

Download and install the latest version of CircuitPython for the Raspberry Pi Pico W from the [Adafruit website](https://circuitpython.org/board/raspberry_pi_pico_w/). After flashing CircuitPython, the microcontroller will appear as a USB drive named `CIRCUITPY`. It expects a file named `code.py` in the root directory, which will be executed automatically when the device is powered on.

Use `picocom /dev/ttyACM0` to access the serial port of the microcontroller. Make sure to adjust the device path if necessary.
To exit, press `Ctrl + A` followed by `q`.

Use the `deploy.sh` script to synchronize your local project with the CIRCUITPY drive. Make sure to adjust the destination path in the script according to your Linux distribution. This prevents developing directly on the CIRCUITPY drive, which can lead to issues with file corruption, performance, lack of space and potential data loss. **It also allows you to use version control and other development tools on your local machine.**

The code in the `wifiControl.py` expects you to have a `settings.toml` file (that acts as an environment file) in the root directory of the CIRCUITPY drive with the following structure:

```toml
CIRCUITPY_WIFI_SSID = "Your_WiFi_SSID"
CIRCUITPY_WIFI_PASSWORD = "Your_WiFi_Password"
```

## Files
- `code.py`: Main entry point for the robot. It lets you select which behaviour to run (obstacle avoidance or wifi control) by pressing the corresponding buttons on the robot.

- `obstacleAvoidance.py`: Implements a simple obstacle avoidance behaviour using the ultrasonic sensor. The robot moves forward until it detects an obstacle within a certain distance, at which point it turns right and continues moving. 

- `wifiControl.py`: Implements a simple web server that allows you to control the robot remotely via WiFi. The server provides endpoints for moving forward, backward, left, and right, plus wheel calibration and speed controls.

- `deploy.sh`: A simple bash script to synchronize the local project with the CIRCUITPY drive. Good for development and prevents issues with developing directly on the CIRCUITPY drive.

- `static`: Contains static files for the web server, such as the HTML, CSS, and JavaScript for the control interface.

## Libraries
The code relies on the following libraries, which should be placed in the `lib` directory of the CIRCUITPY drive:
- `adafruit_motor`
- `adafruit_hcsr04`
- `adafruit_httpserver`

> [!IMPORTANT]
> Some of your usual Python libraries may not be available in CircuitPython, and you may need to find alternatives or implement certain functionalities yourself. 
> An example of this is `random`, which does not have `random.sample`, or even language features like `dict.items()` returning different orderings respective to Python. 

## Resources

- Build guide: https://www.cytron.io/tutorial/build-bocobot-car-with-robo-pico

- Getting started and guided examples for several of the kit's components: https://www.cytron.io/tutorial/get-started-robo-pico-circuitpython-setting-up-robo-pico?r=1

- Code examples: https://github.com/CytronTechnologies/Robo-Pico-Kit-CircuitPython/tree/main
