import socket
import json
import argparse
import logging
import select
import struct
import time



def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', 
        dest="port", 
        type=int, 
        default='9999',
        help='port number to listen on')
    parser.add_argument('--loglevel', '-l', 
        dest="loglevel",
        choices=['DEBUG','INFO','WARN','ERROR', 'CRITICAL'], 
        default='INFO',
        help='log level')
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()      # parse the command-line arguments

    # set up logging
    log = logging.getLogger("myLogger")
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    level = logging.getLevelName(args.loglevel)
    log.setLevel(level)
    log.info(f"running with {args}")
    
    log.debug("waiting for new clients...")
    serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creating a socket
    serverSock.bind(("",args.port)) #binding the socket to the public host and the port
    serverSock.listen() #becomes the server socket

    clientList = []

    while True:

        # HERE'S WHERE YOU NEED TO FILL IN STUFF

        # add server socket and all clients to select()
        read, _, _  = select.select([serverSock] + clientList, [],[])

        for sock in read:
            if sock == serverSock: # new client connection 
                client_socket, client_address = serverSock.accept()
                print("New connection from: ", client_address)
                clientList.append(client_socket) #add new client to the list

            else: # existing clent sent a message
                
                try:
                    # read the first 4 bytes
                    packed_len = sock.recv(4,socket.MSG_WAITALL)
                    if not packed_len: # client disconnected
                        print("Connection closed: ", sock.getpeername())
                        clientList.remove(sock)
                        sock.close()
                        continue

                    # unpack the length of the message
                    message_length = struct.unpack('!I', packed_len) [0]

                    # read the actual message
                    message = sock.recv(message_length,socket.MSG_WAITALL)

                    for recipient in clientList:
                        if recipient != sock and recipient != serverSock:
                            recipient.send(packed_len + message)
                except:
                    print("Error with client: ", sock.getpeername())
                    clientList.remove(sock)
                    sock.close()
                    
                     
if __name__ == "__main__":
    exit(main())

