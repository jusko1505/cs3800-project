# chat_client.py
import sys
import socket
import select
import msvcrt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


def chat_client():
    if (len(sys.argv) < 3):
        print('Usage : python chat_client.py hostname port')
        sys.exit()

    # encryption key
    key = AES.new(b'testkey123456789', AES.MODE_CBC, b'ThisisanIV123456')

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while 1:
        # Get the list sockets which are readable, time-out after 1 s
        ready_to_read = select.select([s], [], [], 1)[0]
        # Gets input from I/0
        if msvcrt.kbhit(): 
            ready_to_read.append(sys.stdin)

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data.decode('utf-8'))
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()

            else:
                # user entered a message
                msg = sys.stdin.readline()
                # send encrypted message
                s.send(key.encrypt(pad(msg.encode('utf-8'), 32)))
                sys.stdout.write('[Me] ')
                sys.stdout.flush()
                

if __name__ == "__main__":
    sys.exit(chat_client())