matricula = bytes([5, 4, 2, 6]) # 4 ultimos digitos da minha matricula -> 212005426

# Codigos do Protocolo de Comunicacao
codigo = {
    'solicita_temp_interna': bytes([0x01, 0x23, 0xC1]) + matricula,  # Temperatura Interna
    'solicita_temp_ref': bytes([0x01, 0x23, 0xC2]) + matricula,      # Temperatura de Referencia
    'le_comandos_usuario': bytes([0x01, 0x23, 0xC3]) + matricula,    # Comandos do usuario
    'envia_sinal_controle': bytes([0x01, 0x16, 0xD1]) + matricula,   # Sinal de controle Int (4 bytes)
    'envia_sinal_ref': bytes([0x01, 0x16, 0xD2]) + matricula,        # Sinal de Referencia Float (4 bytes)
    'envia_sistema_on_off': bytes([0x01, 0x16, 0xD3]) + matricula,   # Estado do Sistema (Ligado = 1 / Desligado = 0)
    'modo_controle_temp_ref': bytes([0x01, 0x16, 0xD4]) + matricula, # Modo de Controle da Temperatura de referencia (Dashboard = 0 / Curva/Terminal = 1) (1 byte)
    'envia_estado_func': bytes([0x01, 0x16, 0xD5]) + matricula,      # Estado de Funcionamento (Funcionando = 1 / Parado = 0)       
    'envia_temp_ambiente': bytes([0x01, 0x16, 0xD6]) + matricula,    # Temperatura Ambiente (Float)
    'envia_cont_tempo': bytes([0x01, 0x16, 0xD7]) + matricula,       # Contador de Tempo (usado no modo de pre-programacao)
    'envia_string_display': bytes([0x01, 0x16, 0xD8]) + matricula    # String do Display LCD para o Dashboard
}