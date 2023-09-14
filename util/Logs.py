import matplotlib.pyplot as plt
import csv

class Logs:   
    def __init__(self):
        self.file = open('log.csv', 'w')
        self.writer = csv.writer(self.file)

    def write(self, linha):
        self.writer.writerow(linha)
    
    def close(self):
        self.file.close()
    
    def plotar_temperaturas(self, datas, temps_ref, temps_internas, temps_ambientes):
        fig, ax = plt.subplots()
        ax.plot(datas, temps_ref, label='Temp Ref')
        ax.plot(datas, temps_internas, label='Temp Interna')
        ax.plot(datas, temps_ambientes, label='Temp Ambiente')
        ax.set_xlabel('Data/Hora')
        ax.set_ylabel('Temperatura')
        ax.set_title('Variação das Temperaturas')
        ax.legend()
        ax.grid(True)
        fig.savefig("temperaturas.png")

    def plotar_acionamento(self, datas, pid_datas):
        fig, ax = plt.subplots()
        ax.plot(datas, pid_datas, label='PID Acionamento')
        ax.set_xlabel('Data/Hora')
        ax.set_ylabel('Valor do Acionamento')
        ax.set_title('Variação do Acionamento dos Atuadores')
        ax.legend()
        ax.grid(True)
        fig.savefig("acionamentos.png")
