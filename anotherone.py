import socket
import sys
import threading
import time

s = socket.socket()
cmdserver_ip = "" ################ ENTER THE SERVER IP YOU WANT LISTENING IN THIS STRING ######################
cmdserver_port = 5050
cmdaddress = (cmdserver_ip, cmdserver_port)
s.bind(cmdaddress)
thread_list = []
thread_recv_list = []

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
            List of available commands: 'portscan' 'open ports' 'nmapscan'
            """)
            continue
        else:
            broadcast(command)


print("Server is starting")
start(cmdaddress)