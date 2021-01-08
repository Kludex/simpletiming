import re

import pytest

from simpletiming import Timer, TimerError

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


class CustomLogger:
    """Simple class used to test custom logging capabilities in Timer"""

    def __init__(self):
        """Store log messages in the .messages attribute"""
        self.messages = ""

    def __call__(self, message):
        """Add a log message to the .messages attribute"""
        self.messages += message


def test_timer_as_decorator(capsys):
    decorated_timewaste()
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_timer_as_context_manager(capsys):
    with Timer(message=TIME_MESSAGE):
        waste_time()
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_explicit_timer(capsys):
    t = Timer(message=TIME_MESSAGE)
    t.start()
    waste_time()
    t.stop()
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""


def test_error_if_timer_not_running():
    t = Timer(message=TIME_MESSAGE)
    with pytest.raises(TimerError):
        t.stop()


def test_access_timer_object_in_context(capsys):
    with Timer(message=TIME_MESSAGE) as t:
        assert isinstance(t, Timer)
        assert t.message.startswith(TIME_PREFIX)
    _, _ = capsys.readouterr()


def test_custom_logger():
    logger = CustomLogger()
    with Timer(message=TIME_MESSAGE, logger=logger):
        waste_time()
    assert RE_TIME_MESSAGE.match(logger.messages)


def test_accumulated_decorator(capsys):
    accumulated_timewaste()
    accumulated_timewaste()

    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_TIME_MESSAGE.match(lines[0])
    assert RE_TIME_MESSAGE.match(lines[1])
    assert stderr == ""


def test_accumulated_context_manager(capsys):
    t = Timer(name="accumulator", message=TIME_MESSAGE)
    with t:
        waste_time()
    with t:
        waste_time()

    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_TIME_MESSAGE.match(lines[0])
    assert RE_TIME_MESSAGE.match(lines[1])
    assert stderr == ""


def test_error_if_restarting_running_timer():
    t = Timer(message=TIME_MESSAGE)
    t.start()
    with pytest.raises(TimerError):
        t.start()


def test_using_name_in_text_without_explicit_timer(capsys):
    name = "NamedTimer"
    with Timer(name=name, message="{name}: {:.2f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert re.match(f"{name}: " + r"0\.\d{2}", stdout)


def test_using_name_in_text_with_explicit_timer(capsys):
    name = "NamedTimer"
    with Timer(name=name, message="{name}: {seconds:.2f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert re.match(f"{name}: " + r"0\.\d{2}", stdout.strip())


def test_using_minutes_attribute_in_text(capsys):
    with Timer(message="{minutes:.1f} minutes"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    assert stdout.strip() == "0.0 minutes"


def test_using_milliseconds_attribute_in_text(capsys):
    with Timer(message="{milliseconds:.0f} {seconds:.3f}"):
        waste_time()

    stdout, stderr = capsys.readouterr()
    milliseconds, _, seconds = stdout.partition(" ")
    assert int(milliseconds) == round(float(seconds) * 1000)
