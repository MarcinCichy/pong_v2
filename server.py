import socket
import _thread
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "localhost"
port = 65432

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for connection")

currentId = "0"
pos = {"id": "0",
       "0": 0,
       "1": 0,
       "ball": (0, 0)} # Data to be sent: player id 0 and his vertical pos 0, same for player id 1, ball pos in tuple

def threaded_client(conn):
    global currentId, pos
    conn.send(message_encode(currentId))
    currentId = "1"
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = message_decode(data)
            if not data:
                conn.send(message_encode("Goodvye"))
                break
            else:
                print(f"Received: {reply}")
                id = reply.get("id")
                pos[id] = reply.get(id)

                if id == "0":
                    new_id = "1"
                    """
                    ball position is going to be calculated on player 0
                    """
                    ball_pos = reply.get("ball")
                    pos["ball"] = ball_pos
                if id == "1":
                    new_id = "0"

                pos["id"] = new_id
                reply = pos
                print(f"Sending: {reply}")

            conn.sendall(message_encode(reply))

        except:
            break


def message_encode(msg):
    msg_json = json.dumps(msg)
    msg_bytes = msg_json.encode("utf-8")
    return msg_bytes


# Function to decode server commands
def message_decode(msg_bytes):
    msg_json = msg_bytes.decode("utf-8")
    msg = json.loads(msg_json)
    return msg


while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")

    _thread.start_new_thread(threaded_client, (conn,))












