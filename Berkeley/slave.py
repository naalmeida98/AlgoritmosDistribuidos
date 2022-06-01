from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket 
import time

#Conexão criada na mesma porta
def initSlave(port = 8080):
  
    # Criando socket "slave" e conectando na porta
    slave = socket.socket()          
    slave.connect(('127.0.0.1', port)) 
  
    print("----- Iniciando slave -----")
    print("Recebendo dados do servidor\n")
    #ajustar os parâmetros
    sendTime = threading.Thread()
    sendTime.start()
  
    print("Recebendo tempo sincronizado com o master.\n")
    #ajustar os parâmetros
    receiveTime = threading.Thread()
    receiveTime.start()  


###############################################################   
   
#INICIALIZAÇÃO
if __name__ == '__main__':  
    initSlave(port = 8080)