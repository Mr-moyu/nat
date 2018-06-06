# -*- coding:utf-8 -*-
import socket  # for sockets
import sys  # for exit
# create an AF_INET, STREAM socket (TCP)
def a():
    #remote
    host = '127.0.0.1'
    #host = '139.199.223.182'
    port = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_ip = socket.gethostbyname( host )
    s.connect((remote_ip,port))

    b=s.recv(40960)
    print(b)
    #local



    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect(('127.0.0.1', 4000))
    s2.sendall(b)
    while 1:
        reply = s2.recv(4096)
        s.send(reply)
        print(reply)
        if reply==b'':
            break

    s.close()



def sendlocal(b):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1',4000))
    s.sendall(b)
    reply = s.recv(409600)
    return reply

while 1:
    a()






