from functools import reduce
from dateutil import parser
import threading
import datetime
import socket
import time

#Conexão criada na mesma porta
def initMaster(port = 8080):
  
    master = socket.socket()
    master.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
    print("----- Iniciando master -----")
        
    master.bind(('', port)) 
    master.listen(10)
    print("-- Servidor de relógio iniciado --\n")
  
    print("- Iniciando conexões -\n")
    #ajustar os parâmetros
    masterThread = threading.Thread()
    masterThread.start()
  
    print("Começando a sincronização paralelamente...\n")
    #ajustar os parâmetros
    syncThread = threading.Thread()
    syncThread.start()
   
   
###############################################################   
   
#INICIALIZAÇÃO
if __name__ == '__main__':
  
    initMaster(port = 8080)