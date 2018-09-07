## front end user interface
import socket
import select
import sys
import pyDes


class client:

    def __init__(self, given_port, server_ip):
        self.ip = server_ip
        self.port = given_port
        self.des_k = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def chat(self):
        """ Client's chat function"""
        self.server.connect((self.ip, self.port))
        self.get_key()
        k = pyDes.des(self.des_k, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
        while True:
            socket_list = [sys.stdin, self.server]
            read_sockets, write_socket, err_socket = select.select(socket_list, [], [])

            for sok in read_sockets:
                if sok == self.server:
                    msg = sok.recv(4096)
                    #ciphertext
                    print(msg)
                    #message decrypt
                    print(k.decrypt(msg))

                else:
                    msg = sys.stdin.readline()
                    sys.stdout.write("[me]")
                    sys.stdout.write(msg)
                    # encrypt msg before sending
                    self.server.send(k.encrypt(msg))
                    sys.stdout.flush()

        self.server.close()

    def get_key(self):
        socket_list = [sys.stdin, self.server]
        read_sockets, write_socket, err_socket = select.select(socket_list, [], [])

        for sok in read_sockets:
            if sok == self.server:
                self.des_k = (sok.recv(64)).encode()
                print("key received")
            else:
                ConnectionAbortedError

if __name__ == "__main__":
    server = str(sys.argv[1])
    port = int(sys.argv[2])

    chat_client = client(port, server)
    chat_client.chat()
