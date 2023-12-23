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
        print(f"Searching for {netName}\n")
        for i in cls.netList:
            print(i[0])
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
        
        self.nets=nets#list(set(nets) | set(self.nets))
        self.portList=portList#list(set(portList) | set(self.portList)) 

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

    def startService(self, netName, startLayer, endLayer, listenPort, nextIP, nextPort):
        source = "master"
        task = "bringup"
        message = f"{netName} {startLayer} {endLayer} {listenPort} {nextIP} {nextPort}"
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
                print(f"Sent to {self.ip}:{self.port} - Task: {task}, Message: {message}")
            except ConnectionRefusedError:
                print(f"Connection to {self.ip}:{self.port} refused. Make sure the server is running.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False

        # Updating the Node.netList for network-wide tracking
        if startLayer == 0:
            new_entry = (netName, self.ip, listenPort)
            if new_entry not in Node.netList:
                Node.netList.append(new_entry)

        # Updating self.nets to track networks on this node
        new_net = (netName, startLayer, endLayer, listenPort, nextIP, nextPort)
        if new_net not in self.nets:
            self.nets.append(new_net)

        # Updating self.portList to track used ports on this node
        if listenPort not in self.portList:
            self.portList.append(listenPort)

        return True


    def endService(self, netName, startLayer, endLayer, listenPort, nextIP, nextPort):
        source="master"
        task="shutdown"
        message=f"{netName} {startLayer} {endLayer} {listenPort} {nextIP} {nextPort}"
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
                print(f"Sent to {self.ip}:{self.port} - Task: {task}, Message: {message}")
            except ConnectionRefusedError:
                print(f"Connection to {self.ip}:{self.port} refused. Make sure the server is running.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        # Updating the Node.netList for network-wide tracking
        if startLayer == 0:
            entry_to_remove = (netName, self.ip, listenPort)
            if entry_to_remove in Node.netList:
                Node.netList.remove(entry_to_remove)

        # Updating self.nets to remove the network from this node
        net_to_remove = (netName, startLayer, endLayer, listenPort, nextIP, nextPort)
        if net_to_remove in self.nets:
            self.nets.remove(net_to_remove)

        # Updating self.portList to free up the port
        if listenPort in self.portList:
            self.portList.remove(listenPort)

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
                print(f"Sent to {self.ip}:{self.port} - Task: {task}!")
            except ConnectionRefusedError:
                print(f"Connection to {self.ip}:{self.port} refused. Make sure the server is running.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        Node.nodeList=list(set(Node.nodeList).discard(self))
        return True

    def __str__(self):
        output = f"Node IP: {self.ip}, Port: {self.port}\n"
        return output


def alive(self, int):
    #if time now = time last talked < int return true
    pass

