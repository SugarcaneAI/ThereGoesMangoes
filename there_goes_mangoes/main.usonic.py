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
    while True:
        while not SENSOR.wait_for_out_of_range():
            dist = 0
            try:
                dist = SENSOR.distance * 100
            except: 
                dist = dist
                continue
            print(f"Distance: {dist:.2f} cm", end="\r")
            if 33 >= (dist) <= 35:
                R1.on()
                sleep(0.25)
                R2.on()
                sleep(0.25)
                R2.off()
                R1.off()
            else:
                R2.off()
                R1.off()
            sleep(0.5)
    print("script ended.")

if __name__ == "__main__":
    main()
