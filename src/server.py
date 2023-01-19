import json
import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.1.101"
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = 0

info1 = {
    "player-id": 0,
    "player-x-pos": 50,
    "player-y-pos": 100,
    "player-keys": 0,
    "keys": [],
    "keysToRemove": []
}

info2 = {
    "player-id": 1,
    "player-x-pos": 900,
    "player-y-pos": 100,
    "player-keys": 0,
    "keys": [],
    "keysToRemove": []

}
pos = [info1, info2]


def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(str(currentId)))
    currentId = 1
    reply = ''
    while True:
        try:
            data = conn.recv(2048)

            if not data:
                print(f"{address} has disconnected")

            reply = json.loads(data.decode('utf-8'))
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + json.dumps(reply))
                keys = []

                for value in reply["keys"]:
                    if value not in keys:
                        keys.append(value)



                plyr_id = int(reply["player-id"])

                # Switchar spelare servern kopplar sig till
                pos[plyr_id] = reply
                if plyr_id == 0:
                    nid = 1
                if plyr_id == 1:
                    nid = 0

                # Lägger till alla nycklar på spelfältet
                keys = [t for t in (set(tuple(i) for i in pos[0]["keys"]))] + [t for t in (set(tuple(i) for i in pos[1]["keys"]))]

                # Tar bort duplicerade nyklar
                keys = [t for t in (set(tuple(i) for i in keys))]
                keysToRemove = [t for t in (set(tuple(i) for i in pos[0]["keysToRemove"]))] + [t for t in (set(tuple(i) for i in pos[1]["keysToRemove"]))]
                keysToRemove = [t for t in (set(tuple(i) for i in keysToRemove))]

                # Tar bort de nyklar som fångats upp eller som har varit på planen för länge
                for key in keysToRemove:
                    if key in keys:
                        keys.remove(key)

                pos[0]["keys"] = keys
                pos[1]["keys"] = keys
                reply = pos[nid]

                reply["keysToRemove"] = []
                print("Sending: " + json.dumps(reply))


            conn.sendall(str.encode(json.dumps(reply)))
        except:
            break

    print("Connection Closed")
    conn.close()


while True:
    conn, address = s.accept()
    print("Connected to: ", address)

    start_new_thread(threaded_client, (conn,))
