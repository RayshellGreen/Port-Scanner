#!/bin/python3

import sys
import socket
import threading
from datetime import datetime

# Define constants
MIN_PORT = 1
MAX_PORT = 1024
THREADS = 50
TIMEOUT = 1

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        result = s.connect_ex((target, port))
        if result == 0:
            print("Port {} is open".format(port))
        s.close()
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()
    except socket.error:
        print("Could not connect to server.")
        sys.exit()

def scan_target(target):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()

    print("-" * 50)
    print("Scanning target: " + target_ip)
    print("Time started: " + str(datetime.now()))
    print("-" * 50)

    threads = []
    for port in range(MIN_PORT, MAX_PORT + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid amount of arguments.")
        print("Syntax: python3 scanner.py <ip>")
        sys.exit()
    
    target = sys.argv[1]
    scan_target(target)