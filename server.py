import sys
import socket
import select
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009

def chat_server():
    # encryption test key
    key = AES.new(b'testkey123456789', AES.MODE_CBC, b'ThisisanIV123456')

    # AF_INET = Address Family that the socket can commuicate with, IPv4, here
    # SOCK_STREAM = TCP socket; SOCK_DGRAM = UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Setting Up Socket Options:
    # SOL_SOCKET = the "level" argument used to manipulate socket options
    # SO_REUSEADDR = permit reuse of local addresses on socket 0/1 -> false/true
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print ("Chat server started on port " + str(PORT))
 
    while 1:
        # Get the list sockets which are ready to be read through select():
        # 1. potentially readable, 2. potentially writable, 3. potential error on socket
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                # Socket.accept() outputs a pair:
                # 1. a new socket object, sockfd that can send and receive data on the connection
                # 2. the address -- a pair (IP address, and client side port)
                sockfd, addr = server_socket.accept()
                
                SOCKET_LIST.append(sockfd)
                print ("Client (%s, %s) connected" % addr)
                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 

                    # receiving data from the socket.
                    # data must be decoded in utf-8 for the message to be received
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        # decrypt and decode the message
                        data = unpad(key.decrypt(data), 32)
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data.decode())  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 


    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send((message.encode(encoding='UTF-8')))
            except Exception as e:
                print("except here" + str(e))
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())   