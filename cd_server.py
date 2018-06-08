import socket
import time
import threading
import queue

store = dict()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 4000))
sock.listen(1)
CONN, ADDRESS = sock.accept()


def listen_out():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 80))
    sock.listen(5)
    while True:
        try:
            conn, address = sock.accept()
            threading.Thread(target=handle_request, args=(conn, address)).start()
        except Exception as e:
            print(e)


def listen_local():
    threading.Thread(target=set_response, args=(CONN,)).start()


def handle_request(conn, address):
    key = '-'.join(address)
    request = queue.Queue()
    response = queue.Queue()
    store[key] = [request, response]
    t1 = threading.Thread(target=set_request, args=(conn, key))
    t2 = threading.Thread(target=get_response, args=(conn, key))
    t3 = threading.Thread(target=get_request, args=(CONN, key))
    t1.start()
    t2.start()
    t3.start()


def set_request(conn, key):
    while True:
        data = conn.recv(4096)
        store[key][1].put(data)


def get_request(conn, key):
    while True:
        data = store[key][1].get()
        conn.send(key + "\r\n\r\n" +data)


def set_response(conn):
    while True:
        data = conn.recv(4096)
        key = data.split("\r\n\r\n")[0]
        store[key][2].put(''.join(data.split("\r\n\r\n")[1:]))


def get_response(conn, key):
    while True:
        data = store[key][2].get()
        conn.send(data)


if __name__ == "__main__":
    t1 = threading.Thread(target=listen_out, args=())
    t2 = threading.Thread(target=listen_local, args=())
    t1.start()
    t2.start()

    t1.join()
    t2.join()


