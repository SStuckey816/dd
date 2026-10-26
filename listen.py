import base64
from scapy.all import *

numberOfBytesInAPacket=50




packets = {}


def process_dns_packet(packet):
    # Verify the packet contains both an IP layer and a DNS layer
    
    if packet[DNS].id == 65532:
        enc = b''
        for key,value in sorted(packets.items()):
            enc += value
        
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(f"{base64.decodebytes(enc).decode()}\n")
        
        return
    
    
    packets[packet[DNS].id] = packet[DNS].ar.rdata[0]
    
sniff(filter="udp port 53", prn=process_dns_packet, store=False)