<h1 align="center">
    <strong>Simple Timing</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/simpletiming" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/simpletiming" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/simpletiming/Test">
        <img src="https://img.shields.io/codecov/c/github/Kludex/simpletiming">
    <br />
    <a href="https://pypi.org/project/simpletiming" target="_blank">
        <img src="https://img.shields.io/pypi/v/simpletiming" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/simpletiming">
    <img src="https://img.shields.io/github/license/Kludex/simpletiming">
</p>

## Installation

``` bash
pip install simpletiming
```

## Usage

###  As decorator

``` Python
from simpletiming import Timer
from time import sleep

@Timer(name="Potato")
def potato():
    sleep(1)

potato()

# Elapsed time: 1.0011 seconds
```

### As object

``` Python
timer = Timer()

timer.start()
sleep(1)
timer.stop()

# Elapsed time 1.0011 seconds
```

### As context manager

``` Python
with Timer(message="Elapsed time: {minutes:0.4f} minutes"):
    sleep(1)

# Elapsed time: 0.0167 minutes
```

### On all class methods

``` Python
@Timer(name="MyClass", message="{name}: {seconds:0.4f} seconds")
class MyClass:
    def potato(self):
        sleep(1)

obj = MyClass()
obj.potato()

# MyClass: 1.0011 seconds
```

## License

This project is licensed under the terms of the MIT license.
