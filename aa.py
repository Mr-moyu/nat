import socket
import threading

def sen(ip):
    print('send beginnnnnnnnnnnnnnnnnnnn')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a = b"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 "
    s.connect(ip)
    s.send(b"HTTP/1.1 200 OK\r\n\r\n")
    s.send(b"<aaaa")
    print('send ok!')

def list(p):
    PORT=80
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('',PORT))
    s.listen(10)
    while 1:
        conn,addr=s.accept()
        buf = conn.recv(1024)
        #send
        ts = threading.Thread(target=sen, args=(addr,))
        ts.start()
        print(addr)
        print(buf)
        conn.close()

tser=threading.Thread(target=list,args=(80,))
tser.start()


