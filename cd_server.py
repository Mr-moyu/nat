import socket
import time
import threading
import queue

store = dict()
tag = "\r\n-----\r\n"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 4000))
sock.listen(1)
CONN, ADDRESS = sock.accept()
print(ADDRESS)
print(CONN.recv(4096).decode('utf-8'))
CONN.send("hello Client".encode('utf-8'))


def listen_out():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 80))
    sock.listen(5)
    while True:
        try:
            conn, address = sock.accept()
            print(address)
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
        print("Server set request: " + data)
        store[key][1].put(data)


def get_request(conn, key):
    while True:
        data = store[key][1].get()
        print("Server get request: " + data)
        conn.send(key + tag + data)


def set_response(conn):
    while True:
        data = conn.recv(4096)
        key = data.split(tag)[0]
        print("Server set response: " + data)
        store[key][2].put(''.join(data.split(tag)[1:]))


def get_response(conn, key):
    while True:
        data = store[key][2].get()
        print("Server get response: " + data)
        conn.send(data)


if __name__ == "__main__":
    t1 = threading.Thread(target=listen_out, args=())
    t2 = threading.Thread(target=listen_local, args=())
    t1.start()
    t2.start()

    t1.join()
    t2.join()
