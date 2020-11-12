import socket
import ticket
import sys
import json

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 12000              # Arbitrary non-privileged port

package = ticket.Pacote()

def SendElectionID():
   package.id = input('Please, inform you ID: ')
   package.secret = None
   package.command = 0
   package.data = input('Please, inform the ElectionID: ')
   packageJSON = {'id': package.id, 'secret': package.secret, 'command': package.command, 'data': package.data} # a real dict.
   #crypto.encryptMessage('PIZZA', messageTest) TESTAR COM CRYPTO
   data = json.dumps(packageJSON)
   return bytes(data,encoding="utf-8") 
# Create a socket (AF_INET means IPv4, SOCK_STREAM means a TCP socket)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    clientSocket.connect((HOST, PORT))
    clientSocket.sendall(SendElectionID())


    # Receive data from the server and shut down
    received = clientSocket.recv(1024)
    received = received.decode("utf-8")

finally:
    clientSocket.close()

#print ("Sent:     {}".format(data))
print ("Received: {}".format(received))

# import ticket
# import socket
# from builtins import input
# import crypto
# import pickle


# HOST = ''                 # Symbolic name meaning all available interfaces
# PORT = 12000              # Arbitrary non-privileged port

# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# clientSocket.connect((HOST, PORT))

# package = ticket.Pacote()

# def sendPackage(package): # tentativa de enviar todo o objeto
#    msg = pickle.dumps(package)
#    clientSocket.send(msg)

# def receivePackage():
#    msg = pickle.loads(clientSocket.recv(1024))
#    return msg


# class Switcher(object):
#    def indirect(self,i):
#       method_name = 'number_'+str(i)
#       method=getattr(self,method_name,lambda :'Invalid')
#       return method()

#    def number_0(self):
#       print('First Pack: Send electionID')
#       package.id = input('Please, type your ID:')
#       package.command = 0
#       package.secret = None
#       package.data = input('Please, type the ElectionID')
#       return package.id

#    def number_1(self):
#       return 'one'

#    def number_2(self):
#       return 'two'
            

# s = Switcher()
# messageTest = "This is basic implementation of Vignere Cipher"
# teste = crypto.encryptMessage('PIZZA', messageTest)
# print(teste)
# clientSocket.send(teste.encode())
# #sendPackage(s.indirect(0))

# modifiedSentence = clientSocket.recv(1024).decode()
# #modifiedSentence = receivePackage

# print ('From Server:', modifiedSentence)

# clientSocket.close()