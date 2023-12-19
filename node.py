import json
import socket
import time

class Node:

    #class variable that tracks all created nodes (alive and dead).
    nodeList=[]

    #class variable that tracks running networks and entry point (netName, entryIp, entryPort)
    netList=[]

    @classmethod
    def findByIp(cls, ip):
        for node in cls.nodeList:
            if node.ip == ip:
                return node
        return False
    
    @classmethod
    def isRunning(cls, netName):
        for i in cls.netList:
            if i[0]==netName:
                return (i[1],i[2])
        return False
    
    @classmethod
    def usable(cls, timeToDeath, ramRequirment):
        #return list of nodes with enough ram and that are still alive. 
        #use helper functions below. 
        pass
    
    def __init__(self, ip, port=1026, cpu=100, ram=8, cpuUtilization=0, ramUtilization=0, nets=[], portList=[]):

        self.ip=ip
        self.port=port

        self.cpu=cpu#in Gflops
        self.ram=ram#in GB
        self.cpuUtilization=cpuUtilization#0-100
        self.ramUtilization=ramUtilization#0-100
        
        self.nets=nets#[(netname, startLayer, endLayer, port, ),...]
        self.portList=portList#[list of used ports] Note:only use ports>=1050

        self.lastUpdated=time.time()#time since this node has checked in.

        Node.nodeList.append(self)

    def update(self, cpuUtilization=0, ramUtilization=0, nets=[], portList=[]):
        self.cpuUtilization=cpuUtilization
        self.ramUtilization=ramUtilization
        
        self.nets=list(set(nets) | set(self.nets))
        self.portList=list(set(portList) | set(self.portList)) 

        self.lastUpdated=time.time()

    def getLastUpdated(self):
        return self.lastUpdated
    
    def getAvailablePort(self):
        for i in range(1050,65634):
            if i not in self.portList:
                return i
        return False
    
    def getNets(self):
        return self.nets
    
    def getPortList(self):
        return self.portList
    
    def canFit(self, required):
        return (self.ram*(1-self.ramUtilization/100))>=required

    def startService(self, listenPort, sendPort, nextIP, netName, startLayer=0, endLayer=None):
        source="master"
        task="bringup"
        message=f"{listenPort} {sendPort} {nextIP} {netName} {startLayer} {endLayer}"
        data = {
        'source': source,
        'task': task,
        'netName': netName,
        'listenPort': listenPort,
        'startLayer': startLayer,
        'message': message
                }
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.ip, self.port))
                sock.sendall(json.dumps(data).encode('utf-8'))
                print(f"Sent to {self.host}:{self.port} - Task: {task}, Message: {message}")
            except ConnectionRefusedError:
                print(f"Connection to {self.host}:{self.port} refused. Make sure the server is running.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        if  startLayer==0:
            Node.netList=list(set(Node.netList).add((netName, self.ip, listenPort)))
        self.nets=list(set(self.nets).add((netName, self.ip, listenPort)))
        self.portList=list(set(self.portList).add(listenPort))
        return True

    def endService(self, listenPort, sendPort, nextIP, netName, startLayer=0, endLayer=None):
        source="master"
        task="shutdown"
        message=f"{listenPort} {sendPort} {nextIP} {netName} {startLayer} {endLayer}"
        data = {
        'source':source,
        'task': task,
        'netName': netName,
        'listenPort': listenPort,
        'startLayer': startLayer,
        'message': message
                }
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.ip, self.port))
                sock.sendall(json.dumps(data).encode('utf-8'))
                print(f"Sent to {self.host}:{self.port} - Task: {task}, Message: {message}")
            except ConnectionRefusedError:
                print(f"Connection to {self.host}:{self.port} refused. Make sure the server is running.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        if  startLayer==0:
                Node.netList=list(set(Node.netList).add((netName, self.ip, listenPort)))
        self.nets=list(set(self.nets).discard((netName, self.ip, listenPort)))
        self.portList=list(set(self.portList).discard(listenPort))
        return True
    
    def nodeReset(self):
        task="reset"
        data={
            'task':task
        }
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.ip, self.port))
                sock.sendall(json.dumps(data).encode('utf-8'))
                print(f"Sent to {self.host}:{self.port} - Task: {task}!")
            except ConnectionRefusedError:
                print(f"Connection to {self.host}:{self.port} refused. Make sure the server is running.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        Node.nodeList=list(set(Node.nodeList).discard(self))
        return True

    def __str__(self):
        output = f"Node Info - IP: {self.ip}, Port: {self.port}\n"
        output += "Running Networks:\n"
        
        # Formatting networks in a 3 column format
        for i, net in enumerate(self.nets):
            output += f"{net[0]:<20} {net[1]:<10} {net[2]:<10}"
            if (i + 1) % 3 == 0:
                output += "\n"
            else:
                output += " | "

        output += "\nUsed Ports:\n"

        # Formatting ports in a 3 column format
        for i, port in enumerate(self.portList):
            output += f"{port:<10}"
            if (i + 1) % 3 == 0:
                output += "\n"
            else:
                output += " | "

        return output

def alive(self, int):
    if time now = time last talked < int return true

