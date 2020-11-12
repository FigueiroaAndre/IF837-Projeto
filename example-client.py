import socket
import time

def sendMsg(msg):
  tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  tcp.connect(('localhost', 3333))
  encodedMsg = msg.encode()
  tcp.send(encodedMsg)
  time.sleep(1)
  tcp.close()

message = str(input('Enter your message: '))
sendMsg(message)