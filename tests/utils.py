import re

from simpletiming import Timer

TIME_PREFIX = "Wasted time:"
RE_TIME_MESSAGE = re.compile(TIME_PREFIX + r" 0\.\d{4} seconds")
TIME_MESSAGE = f"{TIME_PREFIX} {{:.4f}} seconds"


def waste_time(num=1000):
    sum(n ** 2 for n in range(num))


@Timer(message=TIME_MESSAGE)
def decorated_timewaste(num=1000):
    waste_time(num)


@Timer(name="accumulator", message=TIME_MESSAGE)
def accumulated_timewaste(num=1000):
    waste_time(num)


@Timer(name="class", message=TIME_MESSAGE)
class CustomClass:
    def waste_time(self, num=1000):
        waste_time(num)


class CustomLogger:
    """Simple class used to test custom logging capabilities in Timer"""

    def __init__(self):
        """Store log messages in the .messages attribute"""
        self.messages = ""

    def __call__(self, message):
        """Add a log message to the .messages attribute"""
        self.messages += message
