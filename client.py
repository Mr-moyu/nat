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
    b=s.recv(4096)

    #local
    reply=sendlocal(b)
    s.sendall(reply)
    print(s)



def sendlocal(b):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1',80))
    s.sendall(b)
    reply = s.recv(4096)
    return reply

a()






