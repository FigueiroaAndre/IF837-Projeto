import ticket
import socket
from builtins import input
import crypto
import pickle


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 12000              # Arbitrary non-privileged port

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((HOST, PORT))

package = ticket.Pacote()

def sendPackage(package): # tentativa de envia todo o objeto
   msg = pickle.dumps(package)
   clientSocket.send(msg)

def receivePackage():
   msg = pickle.loads(clientSocket.recv(1024))
   return msg


class Switcher(object):
   def indirect(self,i):
      method_name = 'number_'+str(i)
      method=getattr(self,method_name,lambda :'Invalid')
      return method()

   def number_0(self):
      print('First Pack: Send electionID')
      package.id = input('Please, type your ID:')
      package.command = 0
      package.secret = None
      package.data = input('Please, type the ElectionID')
      return package.id

   def number_1(self):
      return 'one'

   def number_2(self):
      return 'two'
            

s = Switcher()
messageTest = "This is basic implementation of Vignere Cipher"
teste = crypto.encryptMessage('PIZZA', messageTest)
print(teste)
clientSocket.send(teste.encode())
#sendPackage(s.indirect(0))

modifiedSentence = clientSocket.recv(1024).decode()
#modifiedSentence = receivePackage

print ('From Server:', modifiedSentence)

clientSocket.close()