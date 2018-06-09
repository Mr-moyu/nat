import socket
import time
import threading
import queue

store = dict()
tag = "\r\n-----\r\n"


def listen_server():
    host = '123.207.14.45'
    port = 4000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_ip = socket.gethostbyname(host)
    server.connect((remote_ip, port))
    server.send("Hello Server".encode('utf-8'))
    print(server.recv(4096).decode('utf-8'))
    while True:
        data = server.recv(409600)
        if data == b'':
            continue
        print("Client get request: " + data.decode('utf-8'))
        threading.Thread(target=handle_request, args=(server, data)).start()


def listen_local(b):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 4000))
    s.sendall(b.encode('utf-8'))
    reply = s.recv(409600)
    return reply


def handle_request(server, data):
    key = data.decode('utf-8').split(tag)[0]
    _data = ''.join(data.decode('utf-8').split(tag)[1:])
    _response = listen_local(_data)
    print(_response)
    # print("Client set response: " + _response.decode('utf-8'))
    response = key + tag + _response.decode('utf-8')
    server.sendall(response.encode('utf-8'))


if __name__ == "__main__":
    t = threading.Thread(target=listen_server)
    t.start()
    t.join()
