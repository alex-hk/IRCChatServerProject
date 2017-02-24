import socket
import sys
import json
import time
import asyncore

UNAME = raw_input("Username: ")
HOST = raw_input("Hostname: ")
PORT = raw_input("Port: ")
saddr = (HOST, int(PORT)) 

class Client(asyncore.dispatcher):
    def __init__(self):
        self.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
        self.connect(saddr)
        print 'Socket connected to ', HOST

    def handle_write(self):
        msg = raw_input(UNAME + ": ")
        data = {'uname': UNAME, 'message': msg}
        udata = json.dumps(data)
        try:
            self.sendall(udata)
        except socket.error:
            print 'Send failed'
            sys.exit()

        if msg == "/quit" or msg == "/exit":
            self.close()
            sys.exit()
    
    def handle_read(self):
        message = self.recv(1024)

asyncore.loop()
