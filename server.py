# -*- coding:utf-8 -*-
import socket
import time
import threading
from multiprocessing import Queue

#接受本机
def listen1(p,Q):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', p))
    sock.listen(5)
    while True:
        conn, address = sock.accept()
        #buf=conn.recv(1024)
        print('wait.....')
        E.wait()
        print('wait End...')
        conn.send(Q.get())

        buf = conn.recv(1024)
        print('server rec:'+str(buf))
        Q.put(buf)





def listen2(p,Q):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', p))
    sock.listen(5)
    while True:
        conn, address = sock.accept()
        buf = conn.recv(1024)
        print(str(p)+'shoudao'+str(buf))
        Q.put(buf)
        E.set()
        time.sleep(5)
        buf=Q.get()
        print(buf)
        conn.send(buf)

E = threading.Event()
Q = Queue()

#接受本机
t1=threading.Thread(target=listen1,args=(8080,Q,))
t1.start()

#接受访问者
t2=threading.Thread(target=listen2,args=(801,Q))
t2.start()
