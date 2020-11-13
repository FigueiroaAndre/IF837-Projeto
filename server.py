import socket
import ticket
import json
import sys 

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 12000              # Arbitrary non-privileged port

def sendPackage(package, socket):
    packageJSON = {'id': package.id, 'secret': package.secret, 'command': package.command, 'data': package.data} # a real dict.
    data = json.dumps(packageJSON)
    socket.send(bytes(data,encoding="utf-8"))
    print('Package sended')

def receivePackage(packageJSON, socket):
    packageReceived = json.loads(packageJSON)

    package.id = packageReceived['id']
    package.secret = packageReceived['secret']
    package.command = packageReceived['command']
    package.data = packageReceived['data']

    print('Package received')
    return package

package = ticket.Pacote()

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to create socket")
    sys.exit()

serverSocket.bind((HOST, PORT))

serverSocket.listen(1)

print ('The server is ready to receive')

while True:

    connectionSocket, addr = serverSocket.accept()

    packageJSON = connectionSocket.recv(1024).decode()
    package = receivePackage(packageJSON, serverSocket)
    
    print(package.id)

    #decodedSentence = crypto.decryptMessage('PIZZA', package)
 
    #connectionSocket.send(package.encode())

    connectionSocket.close()
