import socket
import threading
import time
import select
from functools import reduce
from dateutil import parser
import datetime


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

to_port = 7777
s.connect((host, to_port))

my_id = "0"

s.send(my_id.encode('utf-8'))

leader="-1"


def initiate_election(s):
    
    time.sleep(1)
    
    s.send(my_id.encode('utf-8'))
    
    print("Token enviado: " + my_id)
    print("Eleição iniciada")
    
###################################################
##### INIT MASTER
    
def master(stopThread):
        
    client = {}

    def whatTimeTheClock (connector, address):

        while True:

            timeClockString =  connector.recv(1024).decode()  #recv=  o valor de  retorno é um objeto em bytes ; Para descodificar para a string usa  o decode;
            timeClock = parser.parse(timeClockString)
            timeDifferentWatches =  datetime.datetime.now() - \
                                                        timeClock


            client[address]={
                "timeClock"         : timeClock,
                "timeDifference"    : timeDifferentWatches,
                "connector"         : connector
            }

            print("------ Dados do cliente atualizados com " + str(address) + "-------")
            time.sleep(5)

    def  startConnection(master):
        # encontra a hora do relogio nos clientes/escravos
        while True and stopThread==False:
            masterConnector, address = master.accept() #accept soquete do Python aceita uma solicitação de conexão recebida de um cliente TCP.
            salveAddress = str (address[0] )+ ":" +  str(address[1])

            print ("------ Endereço dos escravos: " + salveAddress + "foi conectado com sucesso! ------")

            currentTread =  threading.Thread( target = whatTimeTheClock, args = (masterConnector, salveAddress, ))

            currentTread.start()

    def getAverageClockDifference():
        currentClient = client.copy()
        timeDifferenceList =  list(cli['timeDifference'] for clientAddress, cli in client.items()) #conferir os parâmetros
        sumOfClockDifference = sum (timeDifferenceList, datetime.timedelta(0,0))

        averageClockDiferrence = sumOfClockDifference/len(client)  #CONFERI

        return averageClockDiferrence

    def synchronizeTheClocks():

        while True and stopThread==False:
            print("\n\n--------------------------------------------------\n")
            print("----- NOVO CICLO INICIADO -----")
            print("----- Número de cliente que precisam ser sincronizados:" + str (len(client)) )

            if len(client) > 0: 
                average_clock_difference = getAverageClockDifference()  
                for client_addr, cli in client.items():
                    try:
                        synchronized_time = \
                            datetime.datetime.now() + \
                                                average_clock_difference
    
                        cli['connector'].send(str(synchronized_time).encode())
    
                    except Exception as error:
                        print("Erro no envio de tempo para " + str(client_addr))
    
            else :
                print("--------- Não há clientes ---------")
    
            print("\n\n") 
            time.sleep(5)

    #Conexão criada na mesma porta
    def initMaster(port = 7777):
    
        master = socket.socket()
        master.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        print("----- Iniciando master -----")
            
        master.bind(('', port)) 
        master.listen(10)
        print("-- Servidor de relógio iniciado --\n")
    
        print("- Iniciando conexões -\n")

        masterThread = threading.Thread(target = startConnection, args = (master, ))
        masterThread.start()
    
        print("Começando a sincronização paralelamente...\n")

        syncThread = threading.Thread(target = synchronizeTheClocks, args = ()) 
        syncThread.start()
    
    
    
    initMaster(port = 7777)   
    
################################################################### 
## INIT SLAVE

def slave(stopThread):
    def startSendingTime(slaveClient):
        try:
            while True and stopThread==False:
                slaveClient.send(str(datetime.datetime.now()).encode())
                print(" ----- Tempo recente recebido com sucesso ------")
                time.sleep(5)
        except:
            print("Master desconectado");

    def startReceivingTime(slaveClient):
        try:
            while True and stopThread==False:
                SynchronizedTime = parser.parse(slaveClient.recv(1024).decode())
                print(" ------------- Tempo sincronizado no cliente é: " + str(SynchronizedTime) + "---------")
        except:
            print("Master desconectado");  

    #Conexão criada na mesma porta
    def initSlave(port = 7777):
    
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

 
    initSlave(port = 7777)
    
############################################################

def Ring_Election_Algorithm(s):
    init = True;

    while True:
        eleicao = False
        initSlave = False 
        stopThreadMaster = False
        stopThreadSlave = False
        
        global leader
        try:
            
            s.settimeout(15)
            received = s.recv(1024)
            s.settimeout(None)
            
            received_token_list = received.decode('utf-8')
        
        except socket.timeout:
            leader = "0"
            if init:
                initiate_election(s)
                init=False
            continue

        #elege o coordenador
        if my_id in received_token_list and "Coordenador: " not in received_token_list and "hello" not in received_token_list:
            eleicao = True
            if leader==my_id:
                stopThreadMaster=True
            leader = max(received_token_list)
            if leader==my_id:
                stopThreadSlave=True
                    
            forwarding_leader = "Coordenador: " + leader
           
            time.sleep(1)
           
            s.send(forwarding_leader.encode('utf-8'))
            
        #aplicação iniciando
        elif my_id not in received_token_list and "Coordenador: " not in received_token_list and "hello" not in received_token_list :
            initSlave = True
            print("Token recebida: " + received_token_list)
            
            leader = "0"
            
            received_token_list = received_token_list + " " + my_id
           
            time.sleep(1)
            
            s.send(received_token_list.encode('utf-8'))
            print("Adicionando token: " + received_token_list)
        
        #alguem caiu, ou alguem entrou   
        elif ("hello" in received_token_list or "Coordenador: " in received_token_list )and leader=="-1"  :
                leader="0"
                # initiate_election(s)

               
        elif "Coordenador: " in received_token_list and leader not in received_token_list :
            print(received_token_list)
           
            le=received_token_list.split()
            leader=le[1]
         
            time.sleep(1)
        
            s.send(received_token_list.encode('utf-8'))


        else :
            if leader=="-1" or leader=="0":
                continue
            else :
                
                print(received_token_list)
                
                communicate = "hello" + " from " + my_id

                time.sleep(1)
      
                s.send(communicate.encode('utf-8'))
                continue
        
       
        
        if my_id==leader and eleicao==True:
            print("Algoritmo do master iniciado");  
            masterThread = threading.Thread(target = master, args = (stopThreadMaster,))   
            masterThread.start()
        elif(my_id!=leader and initSlave==False):
            print("Algoritmo do slave iniciado");
            slaveThread = threading.Thread(target = slave, args = (stopThreadSlave, ))
            slaveThread.start()
        

recv_thread = threading.Thread(target=Ring_Election_Algorithm, args=(s,))
recv_thread.start()
recv_thread.join()
s.close()