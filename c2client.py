import socket
import hostportscanner
import nmap3
import requests
import subprocess

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org').text
        return response
    except Exception as error:
        print(f"Error getting public IP: {error}")

def send_to_server(stuffhere):
    stuffhere = stuffhere.encode("utf-8")
    s.send(stuffhere)

cmdserver_ip = "" ################ ENTER YOUR SERVER IP TO CONNECT TO IN THIS STRING ######################
cmdserver_port = 5050
address = (cmdserver_ip, cmdserver_port)
nmap = nmap3.Nmap()
s = socket.socket()
s.connect((address))

hostname = (socket.gethostname())
public_ip = get_public_ip()
client_send = (f"Client {hostname} joined: {public_ip}").encode("utf-8")
s.send(client_send)
while True:
    command = s.recv(1024).decode("utf-8")
    if command == "stopall":
        break
    elif command == "portscan":
        send_to_server("Initiating port scan. This will take a minute.")
        hostportscanner.main()
        open_ports = str(hostportscanner.open_ports)
        #time_passed = str(hostportscanner.main().timepassed)
        send_to_server(f"Client {hostname} at {public_ip} has open ports: {open_ports}.")
    elif command == "dir":
        print("test")
    elif command == "nmapscan":
        print(f"Initiating nmap scan. This will take a minute")
        nmapresult = nmap.nmap_stealth_scan(target=(socket.gethostbyname(hostname)))
        print(nmapresult)
    else:
        print(command)
    
print("Stop device initiated. Disconnecting")
s.close()