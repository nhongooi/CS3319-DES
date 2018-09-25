
# Python program to implement client side of chat room.
import socket
import select
import sys
import pyDes
import string
import hashlib
import hmac

def start_chat(ip, port):
    # start server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))



    # get des key in plaintext
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            keys = socks.recv(16)
            des_key = keys[:8]
            hmac_key = keys[8:]
        else:
            print("Key not received \nInsecure Connection")
    temp_des = pyDes.des(des_key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

    # loop text
    while True:
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

        for socks in read_sockets:
            if socks == server:
                message = temp_des.decrypt(socks.recv(4096))
                dec_msg = message[:-40]
                hash_msg = message[-40:]
                digest = hmac.new(hmac_key, dec_msg, hashlib.sha1).hexdigest()

                if hmac.compare_digest(hash_msg, digest):
                    print("[Authenticated] " + dec_msg)
                else:
                    print("[False] " + dec_msg)
            else:
                message = sys.stdin.readline()
                message = message[:-1] + hmac.new(hmac_key, message[:-1], hashlib.sha1).hexdigest()
                server.send(temp_des.encrypt(message))
                sys.stdout.flush()
    server.close()


if __name__ == "__main__":
    # get init input
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    start_chat(ip, port)
