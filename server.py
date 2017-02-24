import socket
import sys
import json
import asyncore
import time
import collections

HOST = 'localhost'
PORT = 5555

class ServerHandler(asyncore.dispatcher_with_send):

    def __init__(self, socket, server):
        self.sock = socket
        self.server = server

    def handle_read(self):
        self.data = self.recv(1024)
        self.server.broadcast(self.data)

    def parsemsg(self, data): 
        if data:
            udata = json.loads(data)
            
            umsg = udata["message"]
            uname = udata["uname"]
            localtime = time.localtime(time.time())
            utime = "{}:{}:{} - ".format(localtime.tm_hour, localtime.tm_min, localtime.tm_sec) 
            
            fmsg = utime + uname + ': ' + umsg
            print 'Received message from ' + uname + ': ' + umsg
            print 'Formatted message: ' + fmsg
            if (umsg == "/quit") or (umsg == "/exit"):
                self.close()
                sys.exit()
            return fmsg
    
    def handle_write(self):
        data = parsemsg(self.data)
        self.sendall(fmsg)


class ServerSocket(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
        self.set_reuse_addr()
        self.bind((host, port))
        print 'Socket bound'
        self.listen(5)
        print 'Socket listening on port ', PORT
        self.clients = []

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            print "Connected from ", address
            self.clients.append(ServerHandler(sock, self))

    def handle_close(self):
        self.close()

    def broadcast(self, msg):
        for client in self.clients:
            client.handle_write(msg)

server = ServerSocket(HOST, PORT)
asyncore.loop()
