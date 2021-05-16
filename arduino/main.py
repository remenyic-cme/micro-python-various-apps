import machine
import time
import utime
import random

class Blinker:
    led_pin = machine.Pin(25, machine.Pin.OUT)
    
    def __init__(self, sleep=None):
        assert sleep, "expected sleep arg to be int or float, but received {}".format(sleep)
        self.sleep = sleep
    
    def do_the_blink(self, blinks=None):
        assert blinks, "expected blinks to be int by received {}".format(blinks)
        for i in range(blinks):
            Blinker.led_pin.value(1)
            time.sleep(self.sleep)
            Blinker.led_pin.value(0)
            time.sleep(self.sleep)


class Temperature:
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    
    def print_temp(self):
        reading  = Temperature.sensor_temp.read_u16() * Temperature.conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        print(temperature)

#Blinker(0.3).do_the_blink(10)           
#Temperature().print_temp()


class SonicSensor:
    def __init__(self, pin_trigger=None, pin_echo=None):
        assert isinstance(pin_trigger, int), "Expected pin_trigger to be int but received {}".format(str(type(pin_trigger)))
        assert isinstance(pin_echo, int), "Expected pin_echo to be int but received {}".format(str(type(pin_echo)))
        self.trigger = machine.Pin(pin_trigger, machine.Pin.OUT)
        self.echo = machine.Pin(pin_echo, machine.Pin.IN)

    def __call__(self):
        self.trigger.low()
        utime.sleep_us(2)
        self.trigger.high()
        utime.sleep_us(5)
        self.trigger.low()
        signal_off = 0
        signal_on = 0
        while self.echo.value() == 0:
            signal_off = utime.ticks_us()
        while self.echo.value() == 1:
            signal_on = utime.ticks_us()
        time_passed = signal_on - signal_off
        distance = (time_passed * 0.0343) / 2
        return distance


#print(SonicSensor(pin_echo=11, pin_trigger=10)())


class Motor:    
    def __init__(self, ENABLE=None, IN1=None, IN2=None):
        assert isinstance(ENABLE, int), "Expected ENABLE to be of type integer but received {} of type {}".format("'" + str(ENABLE) + "'", str(type(ENABLE)))
        assert isinstance(IN1, int), "Expected IN1 to be of type integer but received {} of type {}".format("'" + str(IN1) + "'", str(type(IN1)))
        assert isinstance(IN2, int), "Expected IN2 to be of type integer but received {} of type {}".format("'" + str(IN2) + "'", str(type(IN2)))
        
        pin_pwm = machine.Pin(ENABLE, machine.Pin.OUT)
        self.pwm = machine.PWM(pin_pwm)
        self.pin_fwd = machine.Pin(IN1, machine.Pin.OUT)
        self.pin_bck = machine.Pin(IN2, machine.Pin.OUT)
        self.pwm.freq(50)

    def increment_speed(self):
        #self.pwm.duty_u16(0)
        for duty in range(0, 65025, 1):
            self.pwm.duty_u16(duty)
            utime.sleep_us(1)

    def forward(self):
        self.pin_fwd.high()
        self.pin_bck.low()  
        
    def backward(self):
        self.pin_fwd.low()
        self.pin_bck.high()
    
    def stop(self):
        for duty in range(65025, 0, -10):
            self.pwm.duty_u16(duty)
            utime.sleep_us(3)
        self.pin_fwd.low()
        self.pin_bck.low()
    
    def run(self, time=None):
        assert isinstance(time, int), "Expected time to be of type int, but got {}".format(str(type(time)))
        print("running")
        self.forward()
        utime.sleep(time)
        self.stop()
        self.backward()
        utime.sleep(time)
        self.stop()
        print("stopping")

        
#motor_left = Motor(ENABLE=2, IN1=3, IN2=4)
#motor_right = Motor(ENABLE=7, IN1=5, IN2=6)


class Robot:
    
    def __init__(self):
        self.motor_left = Motor(ENABLE=2, IN1=3, IN2=4)
        self.motor_right = Motor(ENABLE=7, IN1=5, IN2=6)
        
        # setting up pwm to 0 for both motor sides
        self.max_pwm = 65025
        self.pwm_left = 0
        self.pwm_right = 0
        self.motor_left.pwm.duty_u16(self.pwm_left)
        self.motor_right.pwm.duty_u16(self.pwm_right)
        
        # setting up the sensors
        self.sens_right = SonicSensor(pin_echo=13, pin_trigger=12)
        self.sens_front = SonicSensor(pin_echo=11, pin_trigger=10)
        self.sens_left = SonicSensor(pin_echo=9, pin_trigger=8)
        
        self.running = False
        self.stop_me = False
    
    
    def set_pwm_left(self, value):
        assert isinstance(value, int), "Expected value to be int but received {} of type {}".format("'" + str(value) + "'", str(type(value)))
        self.pwm_left += value
        print(self.pwm_left)
        self.motor_left.pwm.duty_u16(self.pwm_left)
        
    def set_pwm_right(self, value=None):
        assert isinstance(value, int), "Expected value to be int but received {} of type {}".format("'" + str(value) + "'", str(type(value)))
        self.pwm_right += value
        self.motor_right.pwm.duty_u16(self.pwm_right)
        
    def get_current_pwm(self):
        return sorted([self.pwm_left, self.pwm_right])[0]

    def check_right(self):
        if self.sens_right() < 15:
            return True
        
    def check_left(self):
        if self.sens_left() < 15:
            return True
        
    def move_forward(self):
        if self.check_front():
            return False
        self.motor_left.forward()
        self.motor_right.forward()
        for duty in range(0, 65025, 1):
            self.motor_left.pwm.duty_u16(duty)
            self.motor_right.pwm.duty_u16(duty)
            utime.sleep_us(1)
        return True

    def run2(self):
        self.motor_left.forward()
        self.motor_right.forward()
        while (self.pwm_left < self.max_pwm / 2):
            self.set_pwm_left(100)
            utime.sleep_us(5)
        print("tana")
        utime.sleep(2)
        print(self.get_current_pwm())
        self.stop()

    def run(self):
        if not self.stop_me:
            if not self.move_forward():
                print("Obstacle ahead!")
                if not self.check_left():
                    print("Moving to the left.")
                    utime.sleep_us(50)
                    self.rotate_left()
                    self.run()
                if not self.check_right():
                    print("Moving to the right.")
                    utime.sleep_us(50)
                    self.rotate_right()
                    self.run()
        self.running = True
        if (self.running and not self.stop_me):
            print("moving forward ... ")
            while not self.check_front():
                continue
            print("Stopping now.")
            self.stop()
            self.stop_me = True
        
    def move_backward(self, time=1):
        self.motor_left.backward()
        self.motor_right.backward()
        for duty in range(0, 65025, 1):
            self.motor_left.pwm.duty_u16(duty)
            self.motor_right.pwm.duty_u16(duty)
            utime.sleep_us(1)
        utime.sleep(time)
        self.stop()
        
    def rotate_left(self, time=1):
        self.motor_left.forward()
        self.motor_right.backward()
        for duty in range(0, 65025, 10):
            self.motor_left.pwm.duty_u16(duty)
            self.motor_right.pwm.duty_u16(duty)
            utime.sleep_us(1)


    def rotate_right(self, time=1):
        self.motor_left.backward()
        self.motor_right.forward()
        for duty in range(0, 65025, 10):
            self.motor_left.pwm.duty_u16(duty)
            self.motor_right.pwm.duty_u16(duty)
            utime.sleep_us(1)

        
    def stop(self):
        for duty in range(10, 0, -7):
            self.motor_left.pwm.duty_u16(duty)
            self.motor_right.pwm.duty_u16(duty)
            utime.sleep_us(3)


#Robot().stop()

#Robot().run2()
#Robot().stop()
#Robot().move_backward()
#Robot().rotate_left(100_000)
#Robot().move_forward()s


print("END")

