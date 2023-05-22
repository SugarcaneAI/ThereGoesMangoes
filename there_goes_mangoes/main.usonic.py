import gpiozero as gpio
from time import sleep

R1 = gpio.DigitalOutputDevice(21, initial_value=1)
R2 = gpio.DigitalOutputDevice(20, initial_value=1)

R2.off()
R1.off()

<<<<<<< HEAD
SENSOR = gpio.DistanceSensor(echo=5, trigger=4)
=======
SENSOR = gpio.DistanceSensor(echo=24, trigger=23)
sleep(1)
>>>>>>> 4308dd8ee100f445da22f5e190401faf6a17ee04

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
