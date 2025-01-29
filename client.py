"""
A skeleton from which you should write your client.
"""


import socket
import json
import argparse
import logging
import select
import sys
import time
import datetime
import struct

from message import UnencryptedIMMessage


def parseArgs():
    """
    parse the command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', 
        dest="port", 
        type=int, 
        default='9999',
        help='port number to connect to')
    parser.add_argument('--server', '-s', 
        dest="server", 
        required=True,
        help='server to connect to')       
    parser.add_argument('--nickname', '-n', 
        dest="nickname", 
        required=True,
        help='nickname')                
    parser.add_argument('--loglevel', '-l', 
        dest="loglevel",
        choices=['DEBUG','INFO','WARN','ERROR', 'CRITICAL'], 
        default='INFO',
        help='log level')
    args = parser.parse_args()
    return args


def main():
    args = parseArgs()

    # set up the logger
    log = logging.getLogger("myLogger")
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
    level = logging.getLevelName(args.loglevel)
    
    log.setLevel(level)
    log.info(f"running with {args}")
    
    log.debug(f"connecting to server {args.server}")
    try:
        s = socket.create_connection((args.server,args.port)) 
        log.info("connected to server")
    except:
        log.error("cannot connect")
        exit(1)

    # here's a nice hint for you...
    readSet = [s] + [sys.stdin]

    while True:
        # HERE'S WHERE YOU NEED TO FILL IN STUFF

        # DELETE THE NEXT TWO LINES. It's here now to prevent busy-waiting.
        time.sleep(1)
        log.info("not much happening here.  someone should rewrite this part of the code.")

        

if __name__ == "__main__":
    exit(main())

