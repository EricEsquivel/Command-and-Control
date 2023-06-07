#portscanner by E
#edited version of my 'budgetportscanner' to fit command and control
import socket
import time
import threading

#prep stuff here: check for proper range for starting and ending ports
ip = socket.gethostbyname(socket.gethostname())
firstport = 0
lastport = 65535
portrange = range(firstport,lastport + 1) #set range of ports to scan here
open_ports = [] #Display all open ports in this list
threadslist = []
maxthreads = threading.BoundedSemaphore(value=1000) #make a max of 1000 threads instead of 1 thread per port incase of high port range
starttime = time.time()


#function for making a socket so that function can be called later to make a socket for each individual thread
def portscan(port):
    try:
        s = socket.socket()
        s.settimeout(1)
        if s.connect_ex((ip, port)) == 0:
            open_ports.append(port)
        #else:                                  #   UNCOMMENT HERE TO SEE ALL PORTS THAT ARE CLOSED   #
        #    print(f"{port} closed")            #                   FLOODS CLI                        #
    except Exception as error:
        print(f"Error: {error}")
    finally:
        s.close()
        maxthreads.release()


#for every port in the port range, make a new thread up to 1000 and call function for each one, start it, and add the thread to thread list to call later
def main():
    global open_ports
    open_ports = []
    for everyport in portrange:
        maxthreads.acquire()
        thread = threading.Thread(target=portscan, args=(everyport,))
        thread.start()
        threadslist.append(thread)


    #makes every thread in threadslist stop main thread from executing so that they can finish executing
    for everythread in threadslist:
        thread.join()


    #Display open ports, closed ports, and time taken to finish process
    endtime = time.time()
    timepassed = round(endtime - starttime, 2)