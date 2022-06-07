from functools import reduce
from dateutil import parser
import threading
import datetime
import socket
import time

client = {}

def whatTimeTheClock (address, connector):

    while True:

        timeClockString =  connector.recv(1024).decode()  #recv=  o valor de  retorno é um objeto em bytes ; Para descodificar para a string usa  o decode;
        timeClock= parser.parse(timeClockString)
        timeDifferentWatches=  datetime.datetime.now() - timeClock


        client[address]={
            "timeClock": timeClock,
            "timeDifferentWatches": timeDifferentWatches,
            "connector": connector
        }

        print("------ Dados do cliente atualiados com " + str(address) + "-------")
        time.sleep(5)

def  startConnectin (master):
    # encontra a hora do relogio nos clientes/escravos
    while True:
        masterConnector, address = master.accept() #accept soquete do Python aceita uma solicitação de conexão recebida de um cliente TCP.
        salveAddress = str (address[0] )+ ":" +  str(address[1])

        print ("------ Endereço dos escravos: " + salveAddress + "foi conectado com sucesso! ------")

        currentTread =  threading.Thread( target = whatTimeTheClock, args = (masterConnector,salveAddress,))

        currentTread.start()

def getAverageClockDifference():
    currentClient = client.copy()
    timeDifferenceList =  list(client['timeDifference'] for clientAddress, c in client.items()) #conferir os parâmetros
    sumOfClockDifference = sum (timeDifferenceList, datetime.timedelta(0,0))

    averageClockDiferrence = sumOfClockDifference/len(client)  #CONFERI

    return averageClockDiferrence

def synchronizeTheClocks ():

    while True:
        print("----- Novo ciclo iniciado -----")
        print("----- Número de cliente que precisam ser sicronizados:" + str (len (client)) )

       # if len(client) > 0:

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
    syncThread = threading.Thread() #tem que colocar um parâmetro
    syncThread.start()
   
   
###############################################################   
   
#INICIALIZAÇÃO
if __name__ == '__main__':
  
    initMaster(port = 8080)