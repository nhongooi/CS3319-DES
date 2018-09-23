
import socket
import select
import sys
from random import choice
from string import ascii_letters
from thread import *

list_of_clients = []


def server_online(port, num_conn):

    ip = socket.gethostbyname(socket.gethostname())
    des_key = gen_key()
    hmac_key = gen_key()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(num_conn)

    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print addr[0] + " connected"

        start_new_thread(clientthread, (conn, addr, des_key, hmac_key))

    conn.close()
    server.close()


def gen_key():
    return "".join([choice(ascii_letters) for x in range(8)])


def clientthread(conn, addr, des_key, hmac_key):
    # initial key
    conn.send(''.join((des_key, hmac_key)))

    while True:
            try:
                message = conn.recv(4096)
                if message:
                    print "<" + addr[0] + "> " + message

                    broadcast(message, conn)
                else:
                    remove(conn)
            except:
                continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python <script.py> <port> <number of connections>"
        exit()

    port = int(sys.argv[1])
    conn_num = int(sys.argv[2])

    server_online(port, conn_num)