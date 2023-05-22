import RPi.GPIO as gpio
import timeit

def wait_for_echo(pin: int):
    while not gpio.input(pin):
        continue
    return
