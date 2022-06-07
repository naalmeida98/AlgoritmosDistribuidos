from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket 
import time

def startSendingTime(slaveClient):
    while True:
        slaveClient.send(str(datetime.datetime.now()).encode())
        print(" ----- Tempo recente recebido com sucesso ------")
        time.sleep(5)

def startReceivingTime(slaveClient):
    while True:
        SynchronizedTime = parser.parse(slaveClient.recv(1024).decode())
        print(" ------------- Tempo sincronizado no cliente é: " + str(SynchronizedTime) + "---------")

#Conexão criada na mesma porta
def initSlave(port = 8080):
  
    # Criando socket "slave" e conectando na porta
    slave = socket.socket()          
    slave.connect(('127.0.0.1', port)) 
  
    print("----- Iniciando slave -----")
    print("Recebendo dados do servidor\n")

    sendTime = threading.Thread(target = startSendingTime, args = (slave, ))
    sendTime.start()
  
    print("Recebendo tempo sincronizado com o master.\n")

    receiveTime = threading.Thread(target = startReceivingTime, args = (slave, ))
    receiveTime.start()  


###############################################################   
   
#INICIALIZAÇÃO
if __name__ == '__main__':  
    initSlave(port = 8080)