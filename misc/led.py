import machine
import time
import _thread
import math


def get_board_led():
    return machine.Pin(2, machine.Pin.OUT)


def toggle(led=get_board_led()):
    led.value(not led.value())


def set(led=get_board_led(), _value=1):
    led.value(_value)


class Blink():
    def __init__(self, blink_delay: int = 300, blink_until: int = 0, led=get_board_led()):
        self.led = led
        self.blink_delay = blink_delay
        self.blink_until = blink_until
        self.condition = True

    def __enter__(self):
        _thread.start_new_thread(self.thread_creator, [])

    def thread_creator(self):
        if self.blink_until == 0:
            while self.condition:
                self.blink()
        else:
            for i in range(self.blink_until):
                if self.condition:
                    self.blink()
        self.__exit__("breh", "breh", "breh",)  # breh

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.condition = False
        set(self.led, 0)

    def blink(self):  # blink_delay in ms,if not passed the uses self.blink_delay
        toggle(self.led)
        time.sleep_ms(self.blink_delay)
        toggle(self.led)
        time.sleep_ms(self.blink_delay)


class Fade():
    def __init__(self, fade_delay: int = 100, fade_until: int = 0, freq=1000, led=get_board_led()):
        self.fade_delay = fade_delay
        self.fade_until = fade_until
        self.led = led
        self.pwm_led = machine.PWM(led, freq=freq)
        self.condition = True

    def __enter__(self):
        try:
            _thread.start_new_thread(self.thread_creator, [])
        except KeyboardInterrupt:
            self.condition = False

    def thread_creator(self):
        if self.fade_until == 0:
            while self.condition:
                self.fade()
                time.sleep_ms(self.fade_delay)
        else:
            for i in range(self.blink_until):
                if self.condition:
                    self.fade()
                    time.sleep_ms(self.fade_delay)
        _thread.exit()  # dont think this is ever executed

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.condition = False
        self.pwm_led.deinit()
        set(self.led, 0)

    def fade(self):
        for i in range(21):
            if not self.condition:
                _thread.exit()
            self.pwm_led.duty(1000-int(math.cos(i / 10 * math.pi) * 500 + 500)) 
            time.sleep_ms(50)


class Glow:
    def __init__(self, led=get_board_led()):
        self.led = led

    def __enter__(self):
        set(self.led, 0)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        set(self.led, 0)
