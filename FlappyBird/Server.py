import socket
from _thread import *
from packets import Packet
import struct
import msgpack
from GlobalInfo import GlobalInfo

server = GlobalInfo.server
port = GlobalInfo.port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)


s.listen()
print("Waiting for a connection, Server Started")


packets:list[Packet] = []
missedCount:list[int] = []

def GetReadyCount():
    readyCount = 0
    for packet in packets:
        if packet is None:
            continue
        
        if packet.isReady:
            readyCount += 1
            
    return readyCount


def GetConnectedClientsCount():
    count = 0
    for client in packets:
        if client is not None:
            count += 1
    
    return count


def UpdatePacketsServerInfo():
    readyCount = GetReadyCount()
    playerCount = GetConnectedClientsCount()
    for i in range(len(packets)):
        if packets[i] is None:
            continue
        packets[i].readyCount = readyCount
        packets[i].playerCount = playerCount

def GetOtherClients(clientNum):
    clients = []
    i = -1
    for packet in packets:
        i = i + 1
        if packet is None:
            continue
        if clientNum == i:
            continue
        
        clients.append(packet)
    
    return clients

def threaded_client(conn, packetNum:int):
    if packetNum < 0 or packetNum >= len(packets):
        packets.append(Packet())
        missedCount.append(0)
    else:
        packets[packetNum] = Packet()
        missedCount[packetNum] = 0
        
    _send_msg(conn,packets[packetNum].ConvertToJSON())
    reply = ""
    while True:
        UpdatePacketsServerInfo()
        try:
            data = _recv_msg(conn)
            if not data:
                missedCount[packetNum] += 1
                if missedCount[packetNum] < 30:
                    continue
                print("Disconnected")
                break
            else:
                missedCount[packetNum] = 0
                packets[packetNum] = Packet.ConvertFromJSON(data)
                reply = GetOtherClients(packetNum)
                replyDict =  [packet.ConvertToJSON() for packet in reply]
                print("Received: ", data)
                print("Sending : ", replyDict)

            _send_msg(conn,replyDict)
        except:
            break

    print("Lost connection")
    HandleDisconnection(packetNum)
    conn.close()
    
def HandleDisconnection(connectionNum):
    packets[connectionNum] = None

def _send_msg(sock, data):
    try:
        packed = msgpack.packb(data)
        length = len(packed)
        # Prefix the packet with a 4-byte length header
        sock.sendall(struct.pack('>I', length) + packed)
    except:
        print("Error when sending message")
        

def _recv_msg(sock):
    if sock is None:
        return None
    try:
        # Loop to guarantee we read the full 4-byte length header
        raw_length = bytearray()
        while len(raw_length) < 4:
            packet = sock.recv(4 - len(raw_length))
            if not packet:
                return None
            raw_length.extend(packet)
            
        length = struct.unpack('>I', bytes(raw_length))[0]
        
        # Loop to guarantee we read the full message payload
        data = bytearray()
        while len(data) < length:
            packet = sock.recv(min(length - len(data), 4096))
            if not packet:
                return None
            data.extend(packet)
            
        return msgpack.unpackb(bytes(data))
    except Exception as e:
        print(f"Recv error: {e}") # Uncomment for debugging if needed
        return None

clientNum = 0
connectionNum = 0
while True:
    print("Waiting")
    conn, addr = s.accept()
    print("Connected to:", addr)
    connectionNum = 0
    while connectionNum < clientNum:
        if packets[connectionNum] is None:
            break
        connectionNum += 1
        
    start_new_thread(threaded_client, (conn, connectionNum))
    if connectionNum >= clientNum:  
        clientNum += 1