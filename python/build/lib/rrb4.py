# rrb4.py Library

import RPi.GPIO as GPIO
import time

class RRB4:

    RIGHT_SPEED_PIN = 23
    RIGHT_DIR_PIN = 27
    LEFT_SPEED_PIN = 24
    LEFT_DIR_PIN = 22
    SW1_PIN = 20
    SW2_PIN = 26
    LED1_PIN = 12
    LED2_PIN = 21
    TRIGGER_PIN = 17
    ECHO_PIN = 18
    SERVO_1_PIN = 16
    SERVO_2_PIN = 19
    
    pwm_scale = 0
    right_pwm = 0
    left_pwm = 0
    
    delay = 0.05
    reverse_delay = 0.1
    
    old_r_dir = -9
    old_l_dir = -9
    old_r2_dir = -9
    old_l2_dir = -9
    

    def __init__(self, battery_voltage=6.0, motor_voltage=6.0):

        self.pwm_scale = float(motor_voltage) / float(battery_voltage)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.RIGHT_SPEED_PIN, GPIO.OUT)
        self.right_pwm = GPIO.PWM(self.RIGHT_SPEED_PIN, 500)
        self.right_pwm.start(0)
        GPIO.setup(self.RIGHT_DIR_PIN, GPIO.OUT)

        GPIO.setup(self.LEFT_SPEED_PIN, GPIO.OUT)
        self.left_pwm = GPIO.PWM(self.LEFT_SPEED_PIN, 500)
        self.left_pwm.start(0)
        GPIO.setup(self.LEFT_DIR_PIN, GPIO.OUT)

        GPIO.setup(self.SW1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SW2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)
        
        GPIO.setup(self.LED1_PIN, GPIO.OUT)
        GPIO.setup(self.LED2_PIN, GPIO.OUT)
        
    def _speed_direction_to_duty(self, speed, direction):
        if direction == 1:
            speed = 1.0 - speed
        duty = speed * 100 * self.pwm_scale
        return duty
        

    def set_R(self, speed):
        direction = (speed > 0)
        speed = abs(speed)
        if direction != self.old_r_dir:
            time.sleep(self.reverse_delay)
            old_r_dir = direction
        GPIO.output(self.RIGHT_DIR_PIN, direction)
        self.right_pwm.ChangeDutyCycle(self._speed_direction_to_duty(speed, direction))
        time.sleep(self.delay)
    
    def set_L(self, speed):
        direction = (speed > 0)
        speed = abs(speed)
        if direction != self.old_l_dir:
            time.sleep(self.reverse_delay)
            old_l_dir = direction
        GPIO.output(self.LEFT_DIR_PIN, direction)
        self.left_pwm.ChangeDutyCycle(self._speed_direction_to_duty(speed, direction))
        time.sleep(self.delay)
      
    # Deprecated. Kept for compatability with V3 use set_L, set_R
    def set_motors(self, left_pwm, left_dir, right_pwm, right_dir):
        if left_dir:
            left_pwm = -left_pwm
        self.set_L(left_pwm)
        if right_dir:
            right_pwm = - right_pwm
        self.set_R(right_pwm)


    def forward(self, seconds=0, speed=1.0):
        self.set_motors(speed, 0, speed, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def stop(self):
        self.set_motors(0, 0, 0, 0)

    def reverse(self, seconds=0, speed=1.0):
        self.set_motors(speed, 1, speed, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def left(self, seconds=0, speed=0.5):
        self.set_motors(speed, 0, speed, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def right(self, seconds=0, speed=0.5):
        self.set_motors(speed, 1, speed, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def step_forward(self, delay, num_steps):
        for i in range(0, num_steps):
            self.set_driver_pins(1, 1, 1, 0)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 0)
            time.sleep(delay)
        self.set_driver_pins(0, 0, 0, 0)

    def step_reverse(self, delay, num_steps):
        for i in range(0, num_steps):
            self.set_driver_pins(1, 0, 1, 0)
            time.sleep(delay)
            self.set_driver_pins(1, 0, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 1)
            time.sleep(delay)
            self.set_driver_pins(1, 1, 1, 0)
            time.sleep(delay)
        self.set_driver_pins(0, 0, 0, 0)

    def sw1_closed(self):
        return not GPIO.input(self.SW1_PIN) 

    def sw2_closed(self):
        return not GPIO.input(self.SW2_PIN)

    def set_led1(self, state):
        GPIO.output(self.LED1_PIN, state)

    def set_led2(self, state):
        GPIO.output(self.LED2_PIN, state)


    def _send_trigger_pulse(self):
        GPIO.output(self.TRIGGER_PIN, True)
        time.sleep(0.0001)
        GPIO.output(self.TRIGGER_PIN, False)

    def _wait_for_echo(self, value, timeout):
        count = timeout
        while GPIO.input(self.ECHO_PIN) != value and count > 0:
            count -= 1

    def get_distance(self):
        self._send_trigger_pulse()
        self._wait_for_echo(True, 10000)
        start = time.time()
        self._wait_for_echo(False, 10000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len / 0.000058
        return distance_cm

    def cleanup(self):
        GPIO.cleanup()


    

