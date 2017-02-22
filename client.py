import socket
import sys
import json
import time

UNAME = raw_input("Username: ")
HOST = raw_input("Hostname: ")
PORT = raw_input("Port: ")
saddr = (HOST, int(PORT)) 

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Socket failed. Error Code: ' + str(msg[0]) + ' Error Message: ' + msg[1]

print 'Socket Created Successfully'

s.connect(saddr)

print 'Socket Connected to ' + HOST + ' on port ' + PORT

while 1:
    msg = raw_input(UNAME + ": ")
    data = '{"uname": UNAME, "message": msg}'
    try:
        s.sendall(data)
    except socket.error:
        print 'Send failed'
        sys.exit()

    if msg == "/quit" or msg == "/exit":
       s.close()
       sys.exit()

    reply = recv(1024)
    print reply
