import RPi.GPIO as GPIO
import threading

class AirFryer(threading.Thread):
    def __init__(self) -> None:
        super().__init__()

        # Resistor e Ventoinha
        resistor_gpio = 23
        ventoinha_gpio = 24

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(resistor_gpio, GPIO.OUT)
        GPIO.setup(ventoinha_gpio, GPIO.OUT)

        self.resistor = GPIO.PWM(resistor_gpio, 1000)
        self.resistor.start(0)

        self.ventoinha = GPIO.PWM(ventoinha_gpio, 1000)
        self.ventoinha.start(0)
    
    def aquecer_airfryer(self, pid):
        self.resistor.ChangeDutyCycle(pid)

    def resfriar_airfryer(self, pid):
        self.ventoinha.ChangeDutyCycle(pid) 