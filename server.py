from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

host = '0.0.0.0' ####
serverPort = 8080
serverSocket.bind((host, serverPort))
serverSocket.listen(10)

while True:
    
    serverSocket.close()
    sys.exit()