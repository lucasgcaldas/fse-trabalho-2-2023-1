import RPi.GPIO as GPIO
import model.Lcd as Lcd
from time import sleep
import time

GPIO.setmode(GPIO.BCM) 

button = 23
dt = 24
clk = 25 

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)

count = 0
last_call_time = 0
first_state = GPIO.input(clk)
local = [">MANUAL", " AUTOMATICO", " MANUAL", ">AUTOMATICO"]

def read_encoder(channel):
    global count
    global first_state
    global local1, local2

    state_clk = GPIO.input(clk)
    state_dt = GPIO.input(dt)

    if state_clk != first_state:
        if state_dt != state_clk:
            count += 1
            # print(count)
        else:
            count -= 1
            # print(count)
    first_state = state_clk
    if count % 2 == 0:
        local1 = local[0]
        local2 = local[1]
    else:
        local1 = local[2]
        local2 = local[3]        
    
    display_menu(local1, local2)


def read_button(channel):
    global last_call_time
    current_time = time.time()
    print(current_time)

    if current_time - last_call_time <= 0.3:
        print("Pressionado 2x!")
        display_menu("Botao", "Pressionado 2x!")
        last_call_time = 0
    else:
        print("Botao pressionado: ", local1, local2)
        display_menu("Botao pressionado: ", f"{local1} {local2}")
        last_call_time = current_time
    
GPIO.add_event_detect(button, GPIO.FALLING, callback=read_button, bouncetime=200)
GPIO.add_event_detect(clk, GPIO.BOTH, callback=read_encoder) 

# Índice atual do item selecionado
current_item_index = 0

# Função para exibir o menu no display
def display_menu(local1, local2):
    mylcd = Lcd.lcd()
    mylcd.lcd_display_string(local1, 1)
    mylcd.lcd_display_string(local2, 2)

display_menu(local[0], local[1])

try:
    while 1:
        sleep(0.1)

except KeyboardInterrupt:
    pass

GPIO.cleanup()