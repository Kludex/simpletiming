import functools
import inspect
import time
from typing import Callable, Optional


class TimerError(RuntimeError):
    ...


def _timer_decorator(func: Callable, log: Callable):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.perf_counter()
        ret = func(*args, **kwargs)
        last = time.perf_counter() - start
        log(last)
        return ret

    return wrapper_timer


def _class_timer_decorator(cls, log: Callable):
    def decorate():
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, _timer_decorator(getattr(cls, attr), log))
        return cls

    return decorate


def _log(name: Optional[str], message: str, logger: Callable[[str], None]):
    def partial_message(last):
        attributes = {
            "name": name,
            "milliseconds": last * 1000,
            "seconds": last,
            "minutes": last / 60,
        }
        logger(message.format(last, **attributes))

    return partial_message


class Timer:
    _start_time: float
    _log_message = Callable[[Optional[str], str, Callable[[str], None]], None]

    def __init__(
        self,
        name: Optional[str] = None,
        message: str = "Elapsed time: {:0.4f} seconds",
        logger: Callable[[str], None] = print,
    ):
        self._start_time = None
        self._log_message = _log(name, message, logger)

    def start(self):
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")
        self._start_time = time.perf_counter()

    def stop(self):
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it.")
        last = time.perf_counter() - self._start_time
        self._start_time = None
        self._log_message(last)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc_info):
        self.stop()

    def __call__(self, func: Callable):
        if inspect.isclass(func):
            return _class_timer_decorator(func, self._log_message)
        elif callable(func):
            return _timer_decorator(func, self._log_message)
        return func
