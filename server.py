import ticket
import socket
import crypto
import pickle 
import sys 

print("Socket created")
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 12000              # Arbitrary non-privileged port


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

    package = connectionSocket.recv(1024).decode()

    print(package.id)

    decodedSentence = crypto.decryptMessage('PIZZA', package)
 
    connectionSocket.send(package.encode())

    connectionSocket.close()
