[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/mkRAfJmk)
# Trabalho 2 - AirFryer - 2023/1

Trabalho 2 da disciplina de Fundamentos de Sistemas Embarcados (2023/1)

**Aluno:** Lucas Gomes Caldas

**Matrícula:** 212005426

## Como rodar o projeto

- Necessário ```Python3```
- É necessário escolher algum dos dashboards da AirFryer.
- Para entrar na Raspberry Pi: ```ssh <primeiro_nome><ultimo_nome>@<ip> -p 13508``` e a senha é a ```<matricula>```
- Sugestão de configuração de ambiente:
    - ```$ cd [pasta_do_projeto]```
    - ```$ python3 -m venv venv```
    - ```$ source venv/bin/activate```
    - ```$ pip install -r requirements.txt```

### Execução Sistema

- ```$ python3 main.py```

### Execução Encoder

- ```$ python3 extra/encoder_menu.py```

### Estados

#### Iniciando
![2023-06-19_11-06](https://github.com/FGA-FSE/fse-trabalho-2-2023-1-controle-da-airfryer-lucasgcaldas/assets/88175144/82eb5e63-f05c-49d8-8866-48388d596026)

#### Aquecendo ou Resfriando antes de contar o Timer 
![2023-06-19_11-06_1](https://github.com/FGA-FSE/fse-trabalho-2-2023-1-controle-da-airfryer-lucasgcaldas/assets/88175144/9d805574-d2ef-47d9-ba91-7a335ea51fce)

#### Timer/Cronometro
![2023-06-19_11-06_2](https://github.com/FGA-FSE/fse-trabalho-2-2023-1-controle-da-airfryer-lucasgcaldas/assets/88175144/7b06301e-ab93-48d5-b46f-3c3a006756c2)

#### Pareando Temperatura Interna com a Ambiente
![2023-06-19_11-07](https://github.com/FGA-FSE/fse-trabalho-2-2023-1-controle-da-airfryer-lucasgcaldas/assets/88175144/ba9bcc4a-92f4-42b5-a971-06a396dc6fb4)

## Vídeo de entrega

[<img src="https://i.ytimg.com/vi/p0r6N0CWaT0/maxresdefault.jpg">](https://www.youtube.com/watch?v=p0r6N0CWaT0 "FSE - AirFryer")
