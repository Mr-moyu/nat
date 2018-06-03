# -*- coding:utf-8 -*-
import socket
import time
import threading
from multiprocessing import Queue

#8080
def listen1(p,QGET,QRET):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', p))
    sock.listen(5)
    while True:
        try:
            conn, address = sock.accept()
            #GET msg
            msg=QGET.get()
            conn.send(msg)
            conn.settimeout(5)
            print('server wait client..:')
            buf = conn.recv(409600)
            print('server'+str(p)+' rec:'+str(buf))
            QRET.put(buf)
            conn.close()
        except Exception as e:
            print(e)
            continue
#80
def listen2(p,QGET,QRET):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', p))
    sock.listen(5)
    while True:
        try:
            print('wating1.....')
            conn, address = sock.accept()
            buf = conn.recv(409600)
            print('sertver Rece'+str(p)+str(buf))
            #传给8080
            QGET.put(buf)

            print('wating.....')
            buf=QRET.get()
            print('wating end return http...')
            conn.send(buf)
            print('sendok')
            conn.close()
        except Exception as e:
            print(e)
            continue
E = threading.Event()
#外网的htpp包
QGET = Queue()
#从内网返回的包
QRET = Queue()

#接受本机
t1=threading.Thread(target=listen1,args=(8080,QGET,QRET))
t1.start()

#接受访问者
t2=threading.Thread(target=listen2,args=(80,QGET,QRET))
t2.start()
