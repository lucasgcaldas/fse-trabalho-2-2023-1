class Pid:
    def __init__(self):
        self.kp = 30.0                  # Ganho Proporcional
        self.ki = 0.2                   # Ganho Integral
        self.kd = 400.0                 # Ganho Derivativo
        self.t_periodo = 1.0            # Período de Amostragem (ms)

        self.erro_total = 0.0
        self.erro_anterior = 0.0
        self.sinal_de_controle = 0.0
        self.sinal_de_controle_MAX = 100.0
        self.sinal_de_controle_MIN = -100.0

    def calcular_erro(self, referencia, saida_medida):
        return referencia - saida_medida

    def atualizar_erro_total(self, erro):
        self.erro_total += erro

        if self.erro_total >= self.sinal_de_controle_MAX:
            self.erro_total = self.sinal_de_controle_MAX
        elif self.erro_total <= self.sinal_de_controle_MIN:
            self.erro_total = self.sinal_de_controle_MIN

    def calcular_termo_integral(self):
        return self.ki * self.t_periodo * self.erro_total

    def calcular_termo_derivativo(self, erro):
        return self.kd / self.t_periodo * (erro - self.erro_anterior)

    def pid_controle(self, referencia, saida_medida):
        erro = self.calcular_erro(referencia, saida_medida)
        self.atualizar_erro_total(erro)

        termo_integral = self.calcular_termo_integral()
        termo_derivativo = self.calcular_termo_derivativo(erro)

        self.sinal_de_controle = self.kp * erro + termo_integral + termo_derivativo

        if self.sinal_de_controle >= self.sinal_de_controle_MAX:
            self.sinal_de_controle = self.sinal_de_controle_MAX
        elif self.sinal_de_controle <= self.sinal_de_controle_MIN:
            self.sinal_de_controle = self.sinal_de_controle_MIN

        self.erro_anterior = erro

        return self.sinal_de_controle
