from utils import SonicSensor, Motor, time_it
import utime

class Robot:
    MAX_PWM = 65025
    def __init__(self):
        self.motor_left = Motor(enable=2, in1=3, in2=4)
        self.motor_right = Motor(enable=7, in1=5, in2=6)
        self._max_pwm = 65025
        
        # setting up pwm to 0 for both motor sides
        self.motor_left.duty = 0
        self.motor_right.duty = 0
        self._speed = 0
        
        # setting up the sensors
        self.sens_right = SonicSensor(pin_echo=13, pin_trigger=12)
        self.sens_front = SonicSensor(pin_echo=11, pin_trigger=10)
        self.sens_left = SonicSensor(pin_echo=9, pin_trigger=8)
        
        self.GEAR_5 = self._max_pwm
        self.GEAR_4 = self._max_pwm * .8
        self.GEAR_3 = self._max_pwm * .6
        self.GEAR_2 = self._max_pwm * .4
        self.GEAR_1 = self._max_pwm * .3

    def min_duty(self):
        return min([self.motor_left.duty, self.motor_right.duty])
    
    def max_duty(self):
        return max([self.motor_left.duty, self.motor_right.duty])
    
    @property
    def current_speed(self):
        return self._speed
    
    @current_speed.setter
    def current_speed(self, value):
        value = int(value)
        self._speed = value
        self.motor_left.duty = value
        self.motor_right.duty = value
    
    @time_it
    def forward(self):
        self.motor_left.forward()
        self.motor_right.forward()
        
    @time_it
    def backward(self):
        self.motor_left.backward()
        self.motor_right.backward()

    @time_it
    def stop(self):
        speed = self.min_duty()
        if self.current_speed == 0:
            return
        while self.max_duty() > 0:
            self.motor_left.duty -= 75
            self.motor_right.duty -= 75
            utime.sleep_us(3)
            
    @time_it
    def rotate_left(self):
        self.motor_left.backward()
        self.motor_right.forward()

    @time_it
    def rotate_left(self):
        self.motor_left.forward()
        self.motor_right.backward()

@time_it
def main():
    robot = Robot()
    robot.forward()
    robot.current_speed = robot.GEAR_1
    utime.sleep(2)
    robot.current_speed = robot.GEAR_3
    utime.sleep(2)
    robot.rotate_left()
    utime.sleep(2)
    robot.stop()


main()

