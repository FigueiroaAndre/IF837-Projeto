import ticket
import time
from random import randrange

# server = ticket.Server()
# eid = server.createElection('election',['c1','c2'])
# eData = server.getElection(eid)
# print(eData)
# server.startElection(eid)
# eData2 = server.getElection(eid)
# print(eData2)

# def encrypt(plaintext, key):
  # ciphertext = ''
  # for char in plaintext:
    # cipherchar = chr(ord(char) + key)
    # ciphertext = ciphertext + cipherchar
  # return ciphertext
# 
# def decrypt(ciphertext, key):
  # plaintext = ''
  # for char in ciphertext:
    # plainchar = chr(ord(char) - key)
    # plaintext = plaintext + plainchar
  # return plaintext
# 
# message = str(input('Enter a message: '))
# key = 1 + randrange(9)
# encryptedMessage = encrypt(message, key)
# print(f'Encrypted message: {encryptedMessage}')
# decryptedMessage = decrypt(encryptedMessage, key)
# print(f'Decrypted message: {decryptedMessage}')

server = ticket.Server()
server.startServer()
time.sleep(1)
n = 0
while n != 1:
  n = int(input('Type 1 to quit: '))
print('STOP SERVER')
server.stopServer()