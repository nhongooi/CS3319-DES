### Back-end
import socket
import select
import random
import sys
import string
import _thread


class server:

    def __init__(self, server_port, connection_num):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        self.port = server_port
        self.connect_num = connection_num
        self.des_k = self.gen_key()
        self.clients = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host_ip, self.port))
        self.server.listen(self.connect_num)

    def clientThread(self, conn, addr):
        """ Receive and broadcast client's msg"""
        try:
            # send each client connected the same key
            conn.send(self.des_k)
            conn.send("Welcome!")
        except:
            ConnectionAbortedError

        while True:
            try:
                msg = conn.recv(4096)
                if msg:
                    broadcast_msg = "[" + addr[0] + "] " + msg
                    print(broadcast_msg)
                    self.broadcast(broadcast_msg, conn)
                else:
                    self.remove_conn(conn)
            except:
                continue

    def broadcast(self, msg, conn):
        """ Send msg to every client"""
        for client in self.clients:
            if client != conn:
                try:
                    client.send(msg)
                except:
                    client.close()

    def remove_conn(self, conn):
        """ remove connections from client list"""
        if conn in self.clients:
            self.clients.remove(conn)

    def online(self):
        """ Enable the server """
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            print(addr[0], " connected")
            _thread.start_new_thread(self.clientThread, (conn, addr))

    def offline(self):
        """ Turn off server"""
        self.server.close()

    def gen_key(self):
        """ random generate 64 bytes key"""
        return "".join([random.choice(string.ascii_letters) for x in range(8)])


if __name__ == "__main__":
    port = int(sys.argv[1])
    conn_num = int(sys.argv[2])

    chat_server = server(port, conn_num)
    chat_server.online()
    chat_server.offline()
