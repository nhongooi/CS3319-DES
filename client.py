
# Python program to implement client side of chat room.
import socket
import select
import sys
import pyDes


def start_chat(ip, port):
    # start server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    # get des key in plaintext
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            des_key = socks.recv(8)
        else:
            print("Key not received \nInsecure Connection")
    temp_des = pyDes.des(des_key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

    # loop text
    while True:
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                print "Encrypted Message: " + message
                print temp_des.decrypt(message)
            else:
                message = temp_des.encrypt(sys.stdin.readline())
                server.send(message)
                sys.stdout.flush()
    server.close()


if __name__ == "__main__":
    # get init input
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    start_chat(ip, port)
