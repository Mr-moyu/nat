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
    server.send("Hello Server")
    print(server.recv(4096))
    while True:
        data = server.recv(409600)
        print("Client get request: " + data)
        threading.Thread(target=handle_request, args=(server, data))


def listen_local(b):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 4000))
    s.sendall(b)
    reply = s.recv(409600)
    return reply


def handle_request(server, data):
    key = data.split(tag)[0]
    _data = ''.join(data.split(tag)[1:])
    _response = listen_local(_data)
    response = key + tag + _response
    print("Client set response: " + response)
    server.sendall(response)


if __name__ == "__main__":
    t = threading.Thread(target=listen_server)
    t.start()
    t.join()
