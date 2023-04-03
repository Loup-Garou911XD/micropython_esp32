import machine
import time
import _thread


def get_board_led():
    return machine.Pin(2, machine.Pin.OUT)


def toggle(led=get_board_led()):
    led.value(not led.value())


def set(led=get_board_led(), _value=1):
    led.value(_value)


class BlinkLed():
    def __init__(self, blink_delay: int = 300, blink_until: int = 0, led=get_board_led()):
        self.led = led
        self.blink_delay = blink_delay
        self.blink_until = blink_until
        self.condition = True

    def __enter__(self):
        _thread.start_new_thread(self.thread_creator, [])
        pass

    def thread_creator(self):
        if self.blink_until == 0:
            while self.condition:
                self.blink(blink_delay=self.blink_delay)
        else:
            for i in range(self.blink_until):
                if self.condition:
                    self.blink(blink_delay=self.blink_delay)
        self.__exit__("breh", "breh", "breh",)  # breh

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.condition = False
        set(self.led, 0)

    def blink(self, blink_delay=None):  # blink_delay in ms,if not passed the uses self.blink_delay
        if blink_delay == None:
            blink_delay = self.blink_delay
        toggle(self.led)
        time.sleep_ms(blink_delay)
        toggle(self.led)
        time.sleep_ms(blink_delay)


class Glow:
    def __init__(self, led=get_board_led()):
        self.led = led

    def __enter__(self):
        set(self.led, 0)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        set(self.led, 0)
