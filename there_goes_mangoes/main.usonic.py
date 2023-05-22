import gpiozero as gpio
from time import sleep

R1 = gpio.DigitalOutputDevice(21, initial_value=1)
R2 = gpio.DigitalOutputDevice(20, initial_value=1)

R2.off()
R1.off()

SENSOR = gpio.DistanceSensor(echo=24, trigger=23)

R2.on()
R1.on()

def main():
    while True:
        print(f"Distance: {SENSOR.distance * 100:.2f} cm", end="\r")
        if 33 >= (SENSOR.distance * 100) <= 35:
            R1.on()
            sleep(0.25)
            R2.on()
            sleep(0.25)
            R2.off()
            R1.off()
        sleep(0.5)

if __name__ == "__main__":
    main()
