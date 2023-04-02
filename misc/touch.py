from machine import TouchPad, Pin
import _thread
import time


class Touch:

    """     How to use with context manager

from misc import touch 

inited_class=touch.Touch()

with inited_class(touch_callable,off_callabe,timeout_in_ms):

    pass"""

    def __init__(self, pin_no=14, threshold=400):
        self.pin_no = pin_no
        self.threshold = threshold
        self.touchpad = TouchPad(Pin(pin_no))
        self.thread_loop = True  # used to exit out of threaded loop
        # used to exit out of loop in __enter__,i would prefer a better soltion for this
        self.while_touch_loop = True
        self.is_touched = False  # class attribute which is updated after creaton of thread

    def __enter__(self):
        # need to make this threaded because
        # self.while_touch holds thread and
        # __exit__ is never called otherwise
        _thread.start_new_thread(
            self.while_touch, (
                self.on_touch_callable,
                self.off_callable,
                self.timeout)
        )

    def __call__(self, on_touch_callable, off_callable, timeout=1000):
        self.on_touch_callable = on_touch_callable
        self.off_callable = off_callable
        self.timeout = timeout
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.while_touch_loop = False
        self.thread_loop = False

    def thread_creator(self):
        def threaded_func():  # i dont expect to ever use it outside of this method
            while self.thread_loop:
                self.is_touch()
        _thread.start_new_thread(threaded_func, ())

    def is_touch(self):
        try:
            if self.touchpad.read() < self.threshold:
                self.is_touched = True
                return True
            else:
                self.is_touched = False
                return False
        except ValueError:
            pass

    def on_touch(self, callable, *args):
        _thread.start_new_thread(self.thread_creator, ())
        while True:
            if self.is_touched:
                callable(*args)
                self.thread_loop = False
                return

    # if calling without context manager,set self.while_touch_loop to False
    def while_touch(self, on_touch_callable, off_callable, timeout=1000):
        self.thread_creator()
        while self.while_touch_loop:
            if self.is_touched:
                on_touch_callable()
            else:
                off_callable()
            time.sleep_ms(timeout)
        self.thread_loop = False

    def get_touch_pin_number(self):
        return [0, 2, 4, 12, 13, 14, 15, 27, 32, 33]
