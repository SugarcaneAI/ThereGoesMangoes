import gpiozero as gpio
import timeit
from time import sleep

gpio.setmode(gpio.BCM)

gpio.setup()

def wait_for_echo(pin: int):
    while not gpio.input(pin):
        continue
    return

def main():
    while True:
        gpio.output(26, 1)
        sleep(0.00001)
        gpio.output(26, 0)
        

if __name__ == "__main__":
    main()
