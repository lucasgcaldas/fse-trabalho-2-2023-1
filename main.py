from communication.Modbus import codigo
from communication.Uart import Uart
from model.AirFryer import AirFryer
from connection.I2C import I2C
from threading import Thread
from util.Logs import Logs
from util.Pid import Pid
import model.Lcd as Lcd
import datetime
import struct
import time 

LIGAR_AIRFRYER = 1
DESLIGAR_AIRFRYER = 2
LIGAR_SISTEMA = 3
DESLIGAR_SISTEMA = 4
MAIS_TEMPO = 5
MENOS_TEMPO = 6
MENU = 7

i2c = I2C()
uart = Uart()
pid = Pid()
logs = Logs()
air_fryer = AirFryer()
tempo = 0
pid_atual = 0
modo_controle = True # True: manual False: automatico
datas = []
temps_refs = []
temps_internas = []
temps_ambientes = []
pids = []

def main():
    while True:
        response = ler_comandos_usuario()
        
        comandos = {
            LIGAR_AIRFRYER: ligar_airfryer,
            DESLIGAR_AIRFRYER: desligar_airfryer,
            LIGAR_SISTEMA: ligar_sistema,
            DESLIGAR_SISTEMA: desligar_sistema,
            MAIS_TEMPO: mais_tempo,
            MENOS_TEMPO: menos_tempo,
            MENU: menu
        }

        if response in comandos:
            comandos[response]()

        time.sleep(0.2)

def ler_comandos_usuario():  
    print("Esperando comando...")
    mensagem = codigo['le_comandos_usuario']
    uart.escrever(mensagem, len(mensagem))
    
    response = uart.ler()
    time.sleep(0.2)
    response = struct.unpack('i', response)[0]
    print("Comando do usuário: ", response)

    return response

def ligar_airfryer():
    # inicia logs
    cria_logs = Thread(target=registra_log, args=())
    cria_logs.start()

    mensagem = codigo['envia_sistema_on_off'] + b'\x01'
    uart.escrever(mensagem, len(mensagem))
    response = uart.ler()
    time.sleep(0.2)
    response = struct.unpack('i', response)[0]
    print("Liga AirFryer", response)

    message = codigo['modo_controle_temp_ref'] + b'\x00'
    uart.escrever(message, len(message))
    response = uart.ler()
    time.sleep(0.2)
    response = struct.unpack('i', response)[0]
    print("modo setado como manual", response)

    # zera o tempo
    global tempo
    code = struct.pack("<i", int(tempo))
    message = codigo['envia_cont_tempo'] + code
    uart.escrever(message, len(message))

    # envia string para o led
    envia_lcd("Modo Manual", "Iniciando...")

def desligar_airfryer():
    mensagem = codigo['envia_sistema_on_off'] + b'\x00'
    uart.escrever(mensagem, len(mensagem))
    response = uart.ler()
    time.sleep(0.2)
    response = struct.unpack('i', response)[0]
    print("Desliga AirFryer", response)

    # plota graficos
    global datas, temps_refs, temps_internas, temps_ambientes, pids
    logs.plotar_temperaturas(datas, temps_refs, temps_internas, temps_ambientes)
    logs.plotar_acionamento(datas, pids)

    # fecha csv
    logs.close()

def controla_temperatura():
    while True:
        temp_ref = ler_temp_ref()
        temp_interna = ler_temp_interna()
        global pid_atual
        pid_atual = pid.pid_controle(temp_ref, temp_interna)
        print("pid: ", pid_atual)

        # Exibição das temperaturas e mensagem no display LCD
        temp_str = f"TR:{temp_ref} TI:{temp_interna}"
        if pid_atual < 0:
            pid_atual = max(pid_atual * -1, 40)
            print(pid_atual)
            print("Resfriando AirFryer")
            air_fryer.resfriar_airfryer(pid_atual)
            mensagem = "Resfriando..."
        else:
            print("Aquecendo AirFryer")
            air_fryer.aquecer_airfryer(pid_atual)
            mensagem = "Aquecendo..."

        envia_lcd(temp_str, mensagem)
        time.sleep(1)
        response = ler_comandos_usuario()
        if response == DESLIGAR_SISTEMA or int(temp_interna) == int(temp_ref):
            break

def controla_tempo():
    global tempo, modo_controle
    if modo_controle:
        modo = "Manual"
    else:
        modo = "Automatico"

    tempo_seg = tempo * 60
    while tempo_seg > 0:
        temp_ref = ler_temp_ref()
        temp_interna = ler_temp_interna()

        minutos = tempo_seg // 60  # Divide seconds by 60 to get minutes
        segundos = tempo_seg % 60  # Get the remaining seconds
        envia_lcd(f"Timer:{minutos}:{segundos} TR:{temp_ref}", f"TI:{temp_interna} {modo}")
        time.sleep(1)
        tempo_seg -= 1

def controla_temp_ambiente():
    while True:
        temp_ambiente = envia_temp_ambiente()
        temp_interna = ler_temp_interna()
        pid_atual = pid.pid_controle(temp_ambiente, temp_interna)
        print("pid: ", pid_atual)

        # Exibição das temperaturas e mensagem no display LCD
        temp_str = f"TA:{temp_ambiente} TI:{temp_interna}"
        if pid_atual < 0:
            pid_atual = max(pid_atual * -1, 40)
            print(pid_atual)
            print("Resfriando AirFryer")
            air_fryer.resfriar_airfryer(pid_atual)
            mensagem = "Resfriando..."
        else:
            print("Aquecendo AirFryer")
            air_fryer.aquecer_airfryer(pid_atual)
            mensagem = "Aquecendo..."

        envia_lcd(temp_str, mensagem)
        time.sleep(1)
        response = ler_comandos_usuario()
        if response == DESLIGAR_AIRFRYER or int(temp_interna) == int(temp_ambiente):
            break

def ligar_sistema():
    message = codigo['envia_estado_func'] + b'\x01'
    uart.escrever(message, len(message))

    response = uart.ler()
    time.sleep(0.2)
    response = struct.unpack('i', response)[0]
    print("Sistema em funcionamento", response)

    controla_temperatura()
    controla_tempo()
    desligar_sistema()
    controla_temp_ambiente()

def desligar_sistema():
    message = codigo['envia_estado_func'] + b'\x00'
    uart.escrever(message, len(message))

    response = uart.ler()
    time.sleep(0.2)
    response = struct.unpack('i', response)[0]
    print("desligar sistema", response)

    envia_lcd("Sistema Desligado", "Aguardando...")

def mais_tempo():
    global tempo
    tempo += 1
    code = struct.pack("<i", int(tempo))
    message = codigo['envia_cont_tempo'] + code
    uart.escrever(message, len(message))
    print("mais tempo")

def menos_tempo():
    global tempo
    if tempo > 0:
        tempo -= 1
        code = struct.pack("<i", int(tempo))
        message = codigo['envia_cont_tempo'] + code
        uart.escrever(message, len(message))
        print("menos tempo")
    else:
        print("tempo zerado")

def define_temperatura(temperatura):
    code = struct.pack("<f", temperatura)
    message = codigo['envia_sinal_ref'] + code
    uart.escrever(message, len(message))

def define_tempo(tempo):
    code = struct.pack("<i", tempo)
    message = codigo['envia_cont_tempo'] + code
    uart.escrever(message, len(message))

def modo_automatico():
    message = codigo['modo_controle_temp_ref'] + b'\x01'
    uart.escrever(message, len(message))
    response = uart.ler()
    time.sleep(0.2)
    response = struct.unpack('i', response)[0]
    print("modo setado como automatico", response)

    # modo: [temperatura, tempo]
    modos = {
        'pao': [35.00, 5],
        'lasanha': [40.00, 10], 
        'batata': [45.00, 15],
        'frango': [50.00, 20]
    }

    ligar_sistema()
    define_temperatura(modos['frango'][0])
    define_tempo(modos['frango'][1])

    controla_temperatura()
    controla_tempo()
    controla_temp_ambiente()

def menu():
    global modo_controle
    if modo_controle:
        modo_controle = False
        modo_automatico()
    else:
        modo_controle = True
        ligar_sistema()

def envia_lcd(linha_1, linha_2):
    mylcd = Lcd.lcd()
    mylcd.lcd_display_string(linha_1, 1)
    mylcd.lcd_display_string(linha_2, 2)

def ler_temp_ref():
    message = codigo['solicita_temp_ref']

    uart.escrever(message, len(message))
    data = uart.ler()
    temp_ref = round(struct.unpack('f', data)[0], 2)

    print("Temp referencia: ", temp_ref)
    return temp_ref

def ler_temp_interna():
    message = codigo['solicita_temp_interna']

    uart.escrever(message, len(message))
    data = uart.ler()
    temp_interna = round(struct.unpack('f', data)[0], 2)

    print("Temp interna: ", temp_interna)
    return temp_interna

def envia_temp_ambiente():
    temp_ambiente = i2c.get_temperatura()

    code = struct.pack("<f", temp_ambiente)
    message = codigo['envia_temp_ambiente'] + code
    uart.escrever(message, len(message))


    print("Temp ambiente: ", temp_ambiente)
    return temp_ambiente

def registra_log():
        header = ['Data/Hora', 'Temp_Ref', 'Temp_Interna', 'Temp_Ambiente', 'Valor_Acionamento(PID)' ]
        logs.write(header)

        global datas, temps_refs, temps_internas, temps_ambientes, pids
        while True:
            data = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            datas.append(data)

            temp_ref = ler_temp_ref()
            temps_refs.append(temp_ref)

            temp_interna = ler_temp_interna()
            temps_internas.append(temp_ref)
            
            temp_ambiente = i2c.get_temperatura()
            temps_ambientes.append(temp_ambiente)

            global pid_atual
            pids.append(pid_atual)

            line = [data, temp_ref, temp_interna , temp_ambiente, pid_atual]
            logs.write(line) 
            
            time.sleep(1)

if __name__ == "__main__":
    main()