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

def receivePackage(package, socket):
    packageJSON = socket.recv(1024).decode()
    packageReceived = json.loads(packageJSON)

    package.id = packageReceived['id']
    package.secret = packageReceived['secret']
    package.command = packageReceived['command']
    package.data = packageReceived['data']

    print('Package received')
    return package

def sendElectionID(package):
    package.id = input('Please, inform you ID: ')
    package.secret = None
    package.command = 0
    package.data = input('Please, inform the ElectionID: ')
    return package

def main():

    package = ticket.Pacote()

    try:
        # Create a socket (AF_INET means IPv4, SOCK_STREAM means a TCP socket)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Failed to create socket")
        sys.exit()

    try:
        # Connect to server and send data
        clientSocket.connect((HOST, PORT))
        sendPackage(sendElectionID(package), clientSocket)

        # Receive data from the server and shut down
        received = clientSocket.recv(1024)
        received = received.decode("utf-8")

    finally:
        clientSocket.close()

main()