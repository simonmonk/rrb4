# rrb4
Python3 library for the RaspIRobotBoard V4 (RRB4) by MonkMakes

# Installing the Python Libraries

To install the library, issue the following commands 

```
$ cd ~
$ git clone https://github.com/simonmonk/rrb4.git
$ cd rrb4/python
$ sudo python3 setup.py install
```

Attach the RRB4 to your Raspberry Pi. You do not need to attach batteries, motors or anything else to the RRB4 just yet. For now you can just power it through the Pi's normal USB power connector.

Lets run some tests from the Python Console now that everything is installed. We can experiment with the RRB4, even without any motors 

Open a Python console (Python 3) by typing the following into a Terminal window:

```
$ sudo python3
```

Then, within the python console, type the following, one line at a time:

```
from rrb4 import *
rr = RRB4(9, 6)
rr.set_led1(1)
rr.set_led1(0)
rr.set_led2(1)
rr.set_led2(0)
rr.sw1_closed()
```

The last step should display the answer "False" because no switch is attached.

If you prefer, you can use True and False in place of 1 and 0 in the examples above.



# API Reference

## General
The library implements a class called RRB4. This is written for Python 3

To import the library and create an instance of the class, put this at the top of your Python program.

```
from rrb4 import *
rr = RRB4(9, 6)
```
The first parameter '9' is ther battery voltage (6 x 1.5V AA batteries). The second parameter ('6') is the motor voltage (6V for most low cost robot chassis motors). It is important to set these values correctly, as the library will manage the voltage supplied to the motors, to prevent them burning out or running too fast.

The rest is pretty straightforward, there are just a load of useful methods on the class that you can use.

## LEDs

There are two LEDs built-in to the RaspiRobotBoard, called LED1 and LED2. Both of these can be turned on and off using the following methods:

To turn LED1 on just do:

`rr.set_led1(1)`

To turn it off again do:

`rr.set_led1(0)`

To control LED2 just do the same thing but using set_led2.

## Switch Inputs

The sw1_closed() and sw2_closed() functions return true if the contacts for that switch are closed. By default, the switches are open. You can test out closing the switch by shorting the two contacts with a screwdriver.

The following test program will show you the state of each of the switch contacts.

```
from rrb4 import *

rr = RRB4()

while True:
    print("SW1=" + str(rr.sw1_closed()) + " SW2=" + str(rr.sw2_closed()))
```


## Motor (High Level Interface)

There are two levels of command for controlling the motors. There is a high level interface that assumes that the motors are connected to wheels on a rover. These commands are forward, reverse, left, right and stop.

`rr.forward()`

... will start both motors running in the same direction to move the robot rover forwards. They will continue in this direction until another command is issued.

If you want to move forward for a certain amount of time, you can specify a number of seconds as an optional first argument. If you supply a second parameter between 0 and 1 this will control the speed of the motor. This is set to 0.5 as a defaut. If you want the motors to run indefinately, but also want to control the speed, then use 0 as the first patrameter.

Some examples:

```
rr.forward()       # forward half speed indefinately
rr.forward(5)      # forward for 5 seconds at half speed
rr.forward(5, 1)   # forward for 5 seconds at full speed
```

The commands left, right and reverse all work in the same way.

The stop command stops all the motors.



## Motor (Controlling Left and Right Motors)

You can change the speed and direction of each motor separately using the set_L and set_R methods. These functions take a single parameter which is thespeed (0 to 1) and the direction is controlled by the sign.

For example:


```
rr.set_L(1)      # left motor full speed in one direction
rr.set_L(-0.5)   # left motor half speed in the other direction
```


## Motor (Low Level Interface)

The low level interface is intended for control of the motors directly. It allows you to control the speed of each motor and its direction independently.

The method for this (set_motors) takes four arguments: the left speed, left motor direction, right spped and direction.

So to set both motors going forward at full speed, you would just use the following:

`rr.set_motors(1, 0, 1, 0)`

.. and half speed would be:

`rr.set_motors(0.5, 0, 0.5, 0)`

to send the motors both at half speed in opposite directions is:

`rr.set_motors(0.5, 1, 0.5, 0)`




## Stepper Motor Interface

There RRB4 can be used to drive a single bipolar stepper motor with one coil connected to the L motor driver and the other to the R terminals.

Two commands are available to make the motor step in one direction or the other:

```
rr.step_forward(5, 200)  # step in one direction for 200 steps with a 5ms delay between each phase change
rr.set_reverse(5, 200)   # other direction
```



## Range Finder

If you fit the RRB4 with an SR-04 ultrasonic rangefinder, then you can use the following call to measure the distance to the enarest obstacle in cm.

`rr.get_distance()`

## Hardware

You can find the schematic design file in the "design" section of this repo.

The motor controller used is the LV8548MC and you can see the datasheet here: http://www.onsemi.com/pub/Collateral/LV8548MC-D.PDF


## Absolute Maximum Ratings
Input Voltage: 3-12V (6V recommended when driving motors)
Motor Current: 1A per motor
Max current supplied to Pi (excluding motor current): 1A


# Using I2C Displays

The I2C socket is pin compatible with these Adafruit displays: 
+ [4 Digit 7-segment display (red)](http://www.adafruit.com/products/878)
+ [Mini 8x8 LED Matrix (red)](http://www.adafruit.com/products/870)
+ [Bi-color 8x8 LED Matrix (red)](http://www.adafruit.com/products/902)

To use these you will need to download Adafruit's Python library for the Pi from [here](http://learn.adafruit.com/matrix-7-segment-led-backpack-with-the-raspberry-pi/overview).

Make sure that you plug the display in the right way around. The socket pins are labelled on the RRB4, make sure they match up with the labels on the display. You can use male to female jumper wires if you wish to put the display further away or its too big.




# Pin Allocation

The RasPiRobotBoard 4 uses the following Raspberry Pi GPIO pins, (using the BCM notation).

| GPIO Pin      | RRB4 Function  |
| ------------- |-------------| 
| 23      | Motor Right Speed (PWM) | 
| 27      | Motor Right Direction   |  
| 24      | Motor Left Speed (PWM) | 
| 22      | Motor Left Direction   |  
| 20      | SW1    |  
| 26      | SW2    |  
| 12      | LED 1   |  
| 21      | LED 2   |  
| 17      | Rangefinder Trigger  |  
| 18      | Rangefinder Echo  |  
| 16      | Servo 1   |  
| 19      | Servo 2   |  

