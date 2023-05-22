import gpiozero as gpio
from time import sleep

factory = gpio.pins.pigpio.PiGPIOFactory()

R1 = gpio.DigitalOutputDevice(21, initial_value=1)
R2 = gpio.DigitalOutputDevice(20, initial_value=1)

try:
    SENSOR = gpio.DistanceSensor(echo=18, trigger=17, pin_factory=factory, partial=True)
except:
    sleep(1)
    SENSOR = gpio.DistanceSensor(echo=18, trigger=17, pin_factory=factory, partial=True)

def main():
    print("script started.")
    while True:
        R1.off()
        R2.off()
        dist = 0
        try:
            dist = SENSOR.distance * 100
        except: 
            continue
        print(f"Distance: {dist:.2f} cm", end="\r")
        if 33 >= (dist) <= 35:
            R1.on()
            sleep(1)
            R2.on()
            sleep(1)
            R1.off()
            sleep(1)
            R2.off()
            sleep(0.25)
    print("script ended.")

if __name__ == "__main__":
    main()
