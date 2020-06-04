'''Making a online multiplayer game in python'''
import socket
import pickle

class Network:  # Setting up the network class to use in the client
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET is the ipv4 and SOCK_STREAM is tcp
        self.server = "192.168.0.117"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):  # Getting the position of the player
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)  # Connecting to the ip address and port which is our address
            return self.client.recv(2048).decode()  # Receiving connection to the server
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))  # Encoding the data and sending it to the server
            return pickle.loads(self.client.recv(2048))  # Receiving data to the server
        except socket.error as e:
            print(e)
