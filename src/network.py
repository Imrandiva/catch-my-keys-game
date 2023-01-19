import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.1.101"
        self.port = 5555
        self.address = (self.host, self.port)
        self.id = self.start_connection()

    # Starta koppling till servern    
    def start_connection(self):
        self.client.connect(self.address)
        return self.client.recv(2048).decode()

    # Skicka data till server
    def send_data(self, data):

        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
