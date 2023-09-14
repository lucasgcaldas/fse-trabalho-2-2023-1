import serial
import time

from util.Crc16 import calcula_crc

class Uart:
    def __init__(self):
        self.serial = None
        self.esta_conectado = False
        self.conectar()

    def conectar(self):
        if self.serial is not None and self.serial.is_open:
            self.serial.close()

        try:
            self.serial = serial.Serial("/dev/serial0", 9600)
            self.esta_conectado = True
            print('Conexão UART estabelecida...')
        except:
            print('Erro na conexão UART')

    def escrever(self, mensagem, tamanho):
        if self.esta_conectado:
            m1 = mensagem
            m2 = calcula_crc(m1, tamanho).to_bytes(2, 'little')
            msg = m1 + m2
            self.serial.write(msg)
        else:
            self.conectar()

    def ler(self):
        if self.esta_conectado:
            time.sleep(0.5)
            buffer = self.serial.read(9)
            tamanho = len(buffer)

            if tamanho == 9:
                dados = buffer[3:7]

                if self.crc_e_valido(buffer):
                    return dados
                else:
                    print('CRC inválido')
            else:
                print('Mensagem inválida')
        else:
            self.conectar()

        return b'\x00\x00\x00\x00'

    def crc_e_valido(self, buffer):
        crc_recebido = buffer[7:9]
        crc = calcula_crc(buffer[0:7], 7).to_bytes(2, 'little')

        eh_igual = (crc_recebido == crc)
        return eh_igual
