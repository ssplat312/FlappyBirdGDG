import socket
import msgpack
import struct
from packets import Packet
from GlobalInfo import GlobalInfo
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = GlobalInfo.server
        self.port = GlobalInfo.port
        self.addr = (self.server, self.port)
        self.packet = self.connect()
        self.prevPackets = []
        
    def getPacket(self):
        return self.packet

    def connect(self):
        try:
            self.client.connect(self.addr)
            return Packet.ConvertFromJSON(self._recv_msg(self.client))
        except:
            pass

    def send(self, packet:Packet):
        try:
            self._send_msg(self.client, packet.ConvertToJSON())
            packets = self._recv_msg(self.client)
            if packets is None:
                packets = self.prevPackets
            else:
                self.prevPackets = packets
            print("Network Packets")
            print(packets)
            return [Packet.ConvertFromJSON(p_dict) for p_dict in packets if p_dict is not None]
        except socket.error as e:
            print(e)


    def _send_msg(self, sock, data):
        try:
            packed = msgpack.packb(data)
            length = len(packed)
            # Prefix the packet with a 4-byte length header
            sock.sendall(struct.pack('>I', length) + packed)
        except:
            print("Error in sending message")

    def _recv_msg(self,sock):
        if sock is None:
            return None
        try:
            sock.settimeout(.05)
            # Loop to guarantee we read the full 4-byte length header
            raw_length = bytearray()
            while len(raw_length) < 4:
                print("j;")
                packet = sock.recv(4 - len(raw_length))
                print(";jasdf")
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