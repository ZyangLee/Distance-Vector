# timer.py - A timer class
import time


class Timer(object):
    TIMER_STOP = -1

    def __init__(self, duration):
        self._start_time = self.TIMER_STOP
        self._duration = duration

    # Starts the timer
    def start(self):
        if self._start_time == self.TIMER_STOP:
            self._start_time = time.time()

    # Determines whether the timer timed out
    def timeout(self):
        return time.time() - self._start_time >= self._duration

    # 将没有超时的计时器重置
    def refresh(self):
        self._start_time = time.time()
