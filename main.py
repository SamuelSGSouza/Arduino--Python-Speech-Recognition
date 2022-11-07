import serial
import speech_recognition as sr

#Definindo Configurações
porta = "COM3"
velocidade = 9600
recon = sr.Recognizer()
arduino = serial.Serial(porta, velocidade)


def pega_cores(texto):
    cores = ["verde", "amarelo", "vermelho"]
    cores_encontradas = []
    for palavra in texto.split():
        if palavra in cores:
            cores_encontradas.append(palavra)
        elif palavra == "todos" or palavra == "todas" or palavra == "tudo":
            cores_encontradas = cores
    return cores_encontradas

def pega_comandos_e_cores(texto:str):
    texto = texto.lower()
    comandos = ["desligar","ligar", "acender", "apagar", "esperar", "espere"]
    comandos_encontrados = []
    cores_encontradas = []
    dict_comandos = []
    for palavra in texto.split():
        if palavra in comandos:
            comandos_encontrados.append(palavra)
            texto = texto.replace(palavra, "comando-comando", 1)
    texto = texto.strip()
    for idx,comando in enumerate(texto.split('comando-comando')):
        dic = {}
        cores_encontradas = pega_cores(comando)
        numeros_encontrados = [int(s) for s in comando.split() if s.isdigit()]
        if len(cores_encontradas) > 0:
            dic[f"{idx}-"+f'{comandos_encontrados[idx-1]}'] = cores_encontradas
            dict_comandos.append(dic)
        if len(numeros_encontrados) > 0:
            dic[f"{idx}-"+f'{comandos_encontrados[idx-1]}'] = numeros_encontrados
            dict_comandos.append(dic)
    return dict_comandos
   
print(pega_comandos_e_cores("Quero desligar o led vermelho e depois espere 3 segundos e depois ligar o led verde"))

def decide_comando(comando):
    nome_comando = list(comando.keys())[0]
    nome_comando = nome_comando.split("-")[1]
    if nome_comando == "ligar" or nome_comando == "acender":
        return "L"
    elif nome_comando == "desligar" or nome_comando == "apagar":
        return "D"
    elif nome_comando == "esperar" or nome_comando == "espere":
        return "E"
    
def transforma_cores_em_comandos(cores):
    comandos = []
    for cor in cores:
        if cor == "verde":
            comandos.append("a")
        elif cor == "amarelo":
            comandos.append("b")
        elif cor == "vermelho":
            comandos.append("c")
    return comandos

while True:
    with sr.Microphone() as s:
        print("Fale algo: ")
        audio = recon.listen(s)
        try:
            texto = recon.recognize_google(audio, language="pt-BR")
            print("Você disse: " + texto)
            comandos = pega_comandos_e_cores(str(texto).lower())
            for comando in comandos:
                print(comando)
                coma = decide_comando(comando)
                print(coma)
                if coma == "L":
                    cores = transforma_cores_em_comandos(list(comando.values())[0])
                    print(cores)
                    for cor in cores:
                        cor = str(cor).lower()
                        print(cor)
                        arduino.write(cor.encode())
                elif coma == "D":
                    cores = transforma_cores_em_comandos(list(comando.values())[0])
                    for cor in cores:
                        cor = str(cor).upper()
                        print(cor)
                        arduino.write(cor.encode())

        except:
            print()
