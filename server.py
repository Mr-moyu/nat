# -*- coding:utf-8 -*-
import socket
import time
import threading
from multiprocessing import Queue


#1.Chunked无法传输：使用完全准发 client收到4000端口不要包汇总到一起 来一个包转发一个，服务器收到也是来一个转发一个
#2只能转一个包（js那些不能转发）
#发送方关闭tcp的连接,recv()不会阻塞，而是直接返回''

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
            Rbuf=b''
            while 1:
                buf=conn.recv(4096)
                QRET.put(buf)
                #Rbuf=Rbuf+buf
                #if buf==b'':
                    #break
                #print('server'+str(p)+' rec:'+str(buf))

            QRET.put(Rbuf)
            conn.close()
        except Exception as e:
            print(e)
            continue
#80

def handle_request(conn,QGET,QRET):

    buf = conn.recv(4096)
    print('sertver 80 Rece：' + str(buf))
    if buf==b'':
        #抛出异常结束线程
        raise Exception("0byte error")
    # 传给8080
    QGET.put(buf)
    while 1:
        print('wating.....')
        buf2 = QRET.get()
        print('wating end return http:' + str(buf2))
        if buf2 == b'':
            conn.close()
            break
        conn.send(buf2)
        print('sendok')
    conn.close()


def listen2(p,QGET,QRET):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', p))
    sock.listen(5)
    while True:
        try:
            print('wating1.....')
            conn, address = sock.accept()
            #接受到消息新建一个线程
            QGET = Queue()
            QRET = Queue()
            t = threading.Thread(target=handle_request, args=(conn, QGET, QRET))

            t.start()
            print('thread'+t.getName()+'start...')
             # 外网的htpp包
        except Exception as E:
            print(E)

        '''
            buf = conn.recv(409600)
            print('sertver Rece'+str(p)+str(buf))
            #传给8080
            QGET.put(buf)
            while 1:
                print('wating.....')
                buf2=QRET.get()
                print('wating end return http:'+str(buf2))
                if buf2==b'':
                    conn.close()
                    break

                conn.send(buf2)
                print('sendok')
            conn.close()
        except Exception as e:
            print(e)
            continue
        '''

Local = threading.local()
E = threading.Event()
#外网的htpp包
QGET = Queue()
#从内网返回的包
QRET = Queue()

#接受本机
t1=threading.Thread(target=listen1,args=(8080,QGET,QRET))
t1.start()

#接受访问者
t2=threading.Thread(target=listen2,args=(801,QGET,QRET))
t2.start()
