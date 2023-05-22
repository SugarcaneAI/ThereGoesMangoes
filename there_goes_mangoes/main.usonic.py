import gpiozero as gpio
from time import sleep

SENSOR = gpio.DistanceSensor(24, 26)

def main():
    while True:
        print(f"Distance: {SENSOR.distance * 100:.2f} cm", end="\r")
        sleep(0.5)

if __name__ == "__main__":
    main()
