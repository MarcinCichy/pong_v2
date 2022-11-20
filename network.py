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
        data_decode = self.message_decode(data)
        return data_decode


    def send(self, data):
        """
        data: JSON
        """
        try:
            encoded_data = self.message_encode(data)
            self.client.send(encoded_data)  # tutaj nie dałem encodowania, bo otrzymujemy dane w postaci JSONa i wysyałamy je dalej -> zmieniłem żeby kodowało @jaran
            reply = self.message_decode(self.client.recv(BUFFER))
            return reply
        except socket.error as e:
            return str(e)

    @staticmethod
    def message_encode(msg):
        msg_json = json.dumps(msg)
        msg_bytes = msg_json.encode("utf-8")
        return msg_bytes


    # Function to decode server commands
    @staticmethod
    def message_decode(msg_bytes):
        msg_json = msg_bytes.decode("utf-8")
        msg = json.loads(msg_json)
        return msg
