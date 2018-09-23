
# Python program to implement client side of chat room.
import socket
import select
import sys
import pyDes
import string
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

    print "DES key: " + des_key
    print "HMAC key: " + hmac_key
    # loop text
    while True:
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
        digest_maker = hmac.new(hmac_key)

        for socks in read_sockets:
            if socks == server:
                message = temp_des.decrypt(socks.recv(4096))
                dec_msg, hash_msg = message.rstrip().split('=')
                digest = hmac.new(hmac_key, msg=dec_msg.encode('utf-8')).hexdigest()

                print hmac.compare_digest(hash_msg, digest)
                print dec_msg
            else:
                message = sys.stdin.readline()
                digest_maker.update(message)
                message = message[:-1] + '=' + digest_maker.hexdigest()
                server.send(temp_des.encrypt(message.encode('utf-8')))
                sys.stdout.flush()
    server.close()


if __name__ == "__main__":
    # get init input
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    start_chat(ip, port)
