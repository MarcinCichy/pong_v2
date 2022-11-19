import socket
import json

PORT = 65432
BUFFER = 2048
HOST = "127.0.0.1"


class Network:
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.addr = (self.host, self.port)
        self.id = self.connect()
        print(self.id)
    
    def connect(self):
        self.client.connect(self.addr)
        data = self.client.recv(BUFFER)
        data_decode = json.loads(data)  # czy to jest konieczne, i tak dane przesyłane sa przez JSON dalej
        return data_decode
    
    def send(self, data):
        """
        data: JSON
        """
        try:
            self.client.send(
                data)  # tutaj nie dałem encodowania, bo otrzymujemy dane w postaci JSONa i wysyałamy je dalej
            reply = self.client.recv(BUFFER)
            return reply
        except socket.error as e:
            return str(e)
