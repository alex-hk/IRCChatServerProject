import socket
import sys
import json
import asyncore
import time
import collections

HOST = 'localhost'
PORT = 5555

class ServerHandler(asyncore.dispatcher):

    def __init__(self, socket, server):
        asyncore.dispatcher.__init__(self, socket)
        self.server = server
        self.out = collections.deque()
    
    def handle_read(self):
        data = self.recv(1024)
        print 'Received data'
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
                self.server.broadcast(utime + ' - User {} has disconnected'.format(uname))

            #self.sendall(fmsg)
            self.server.broadcast(fmsg)
       

    def say(self, message):
        print 'Putting {} in outbox'.format(message)
        self.out.append(message)

    def handle_write(self):
        if not self.out:
            #print 'Outbox failure'
            return
        msg = self.out.popleft()
        print 'Sending message: ',msg
        self.sendall(msg)


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
            print "Client {} added".format(address)

    def handle_close(self):
        self.close()

    def broadcast(self, msg):
        print 'Broadcasting to all ----------------'
        for client in self.clients:
            print 'Broadcasting to client ',client
            client.say(msg)

server = ServerSocket(HOST, PORT)
asyncore.loop()
