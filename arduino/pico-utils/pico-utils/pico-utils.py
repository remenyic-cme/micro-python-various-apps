import machine
import utime

class SonicSensor2:
    def __init__(self, trigger=None, echo=None):
        """
        SonicSensor class is used to quickly instantiate a sonic sensor
        and have access to multiple built-in functionalities

        :param trigger: integer, must be positive, this is the pin.OUT on your pico
        :param echo: integer, must be positive, this is the pin.IN on your pico
        """

        assert isinstance(trigger, int), "Expected trigger to be int but received {}".format(str(type(trigger)))
        assert isinstance(echo, int), "Expected echo to be int but received {}".format(str(type(echo)))
        self._trigger = machine.Pin(trigger, machine.Pin.OUT)
        self._trigger.value(0)
        self._echo = machine.Pin(echo, machine.Pin.IN)

    def _send_pulse(self):
        """
        Send a pulse and and find out how many microseconds
        it took to travel the distance 1 way
        """
        self._trigger.low()
        utime.sleep_us(2)
        self._trigger.high()
        utime.sleep_us(5)
        self._trigger.low()
        signal_off = 0
        signal_on = 0
        while self._echo.value() == 0:
            signal_off = utime.ticks_us()
        while self._echo.value() == 1:
            signal_on = utime.ticks_us()
        time_passed = signal_on - signal_off
        distance = (time_passed * 0.0343) / 2
        return distance

    @property
    def dist_cm(self):
        """
        This attr sends a pulsse, gets its readings
        and converts them to cm/s using the bellow formula

        distance = pulse duration / 29.1

        Explanation:
            the sound speed on air (343.2 m/s), that It's equivalent to
            0.034320 cm/us that is 1cm each 29.1us


        return distance
        """
        return round(self._send_pulse(), 2)
