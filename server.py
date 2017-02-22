import socket
import sys
import json
import thread

host = 'localhost'
port = 5555
saddr = ('localhost', 5555)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket Created'

try:
    s.bind(saddr)
except socket.error, msg:
    print 'Bind Failed. Error Code: ' + str(msg[0]) + ' Error Message: ' + msg[1]
    sys.exit(1)

print 'Socket Bound'

s.listen(5)

print 'Socket Listening'

def cthreads(user):
    user.send('Test IRC chat. Type \'/help\' for help')

    while True:
        data = user.recv(1024)
        umsg = data[1]

        if not data: break
        localtime = time.localtime(time.time())
        if (umsg == "/quit") or (umsg == "/exit"):
            user.close()
        user.sendall(localtime.tm_hour + ':' + localtime.tm_min + ':' + localtime.tm_sec + ' - ' + data[0] + ': ' + umsg)
    user.close()


while True:
    user, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(cthreads ,(user,))

s.close()

