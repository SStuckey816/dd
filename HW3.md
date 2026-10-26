This HW delves into the fundamentals of network packets and DNS. DNS, or Domain
Name Service, is the phonebook of the internet. It is used to resolve
human-readable URLs into IP address of servers/machines. While this is
the intended use of DNS, it can be abused for other purposes.
This week, you will assume the role of an attacker who has compromised a
client system and needs to extract files to an attacker-controlled server via
DNS requests and responses. This is an actual technique used by attackers,
including APT (Advanced Persistent Threat) groups such as the
[OilRig](https://malpedia.caad.fkie.fraunhofer.de/actor/oilrig), to extract
data from sensitive environments.

This HW will teach you about DNS resolvers and creating raw packets using the
Python `scapy` module. You will then use your knowledge of DNS packets and
their format to build a custom DNS exfiltration tool.

#### DUE DATE: Oct 26, 2026 11:59pm

## Task 1: Set up a simple `dnsmasq` instance and capture the request

You need to create a new `docker-compose.yml`. This will orchestrate 2
containers built from `Dockerfile.client` (this is provided) and `Dockerfile.dns` (this you need to
create). On `Dockerfile.dns`, you will need to set up a working
[`dnsmasq`](https://help.ubuntu.com/community/Dnsmasq) instance that listens
for DNS requests on UDP port 53. You need to figure out how to install
`dnsmasq` (on a Docker container) and configure it (using `/etc/dnsmasq.conf`).

To verify, you will need to query the DNS records of the domain `cs.uic.edu`
via `nslookup`/`dig` (the query happens on `Dockerfile.client`) and capture the
network traffic in `basic-dns.pcap` (the capture happens on `Dockerfile.dns`).

Note:
- Do not modify the container/image names or the subnet or the IP/MAC addresses
  in the `docker-compose.yml`.
- `Dockerfile.client` needs to have the IP address 172.28.10.12
- `Dockerfile.dns` needs to have the IP address 172.28.10.2.
- You will also need to force `Dockerfile.client` to use `Dockerfile.dns` as
  the DNS resolver instead of Docker's default resolver. This can be achieved
  via docker-compose or command line switches in `nslookup`/`dig`.

## Task 2: Build the `exfiltrate.py` and `listener.py` files

You will create a DNS data exfiltrator in a file `/exfiltrate.py` (this will execute
on `Dockerfile.client`). This Python script will read `/secret.txt` from the
`Dockerfile.client` and use the `scapy` Python module to exfiltrate it via DNS
packets. To receive the packets on the other end, you will also need to create
a corresponding `/listener.py` (run on `Dockerfile.dns`) that will listen on
UDP port 53 for the DNS packets, extract the data using the `scapy` module, and
rebuild `/secret.txt`. It is important to note that you will have to work
within the constraints of DNS packets (such as size, encoding, etc.) when
transmitting data. This means that you will have to break the secret into
smaller pieces and send each piece in its own DNS packet.

A typical DNS query packet sent over UDP has a maximum size of 512 bytes. This
allows for roughly 255 bytes of usable space per packet. You will utilize `base64` to
encode the `secret.txt` before breaking it up and sending it over DNS. 
The `secret.txt` given with the HW, after it is base64 encoded, is around 1700 bytes long. The
`/listener.py` will decode the `base64` and rebuild the secret in the correct
order.

It is necessary that the secret is rebuilt in the correct order to receive full
credit. This can be achieved by ordering the DNS queries using Transaction IDs (TxIDs).
The `secret.txt` should be encoded in a linear fashion using transaction IDs low to high.
E.g. the DNS packets containing 
the first few bytes of `secret.txt` can have a TxID of 0x001, next few with a TxID
of 0x002 and so on. The exact TxID don't matter but the order must be ascending.
On the decryption end, `listener.py` will order the packets in ascending order
using TxIDs before decoding it. 

Program should work for any number of Unicode characters in `secret.txt`. 
That is, the program should be able to send and rebuild `secret.txt` of any length
as long as it contains Unicode characters. You can safely assume that the length of secret
will not exceed the maximum number of unique TxIDs. 

To verify, you will need to capture the packets sent by the client in
`exfil-dns.pcap` (the capture happens on `Dockerfile.dns`). Ensure that the
capture runs long enough to capture `secret.txt` given with the homework.

Note:

- All `.py` files need to run in the root directory of their respective
  container.
- DNS packets use UDP, which can be unsynchronized and lossy. While this is
  unlikely to happen in an ideal Docker environment, don't worry about building
  error correction mechanisms in the data transfer. As long as the tool can
  transfer the secret and reassemble it in the correct order, you will receive
  full credit.
- Use a non existent domain `doesnotexist.com` as a base for all queries to ensure 
you don't impact an actual non-root DNS server.

Hint: DNS responses are supposed to return either domain names or IP addresses,
but can they be used to send something else? How would you hide data in domain
URLs? Check out the helpful reading section. 

## Deliverables:
- **basic-dns.pcap**
- **dnsmasq.conf**
- **Dockerfile.dns**
- **exfil-dns.pcap**
- **exfiltrate.py** which is run on `Dockerfile.client` (you don't need to send
  `Dockerfile.client`)
- **listener.py** which is run on `Dockerfile.dns`

#### Helpful readings.
- [Data Exfiltration Over DNS, HTTP & Custom Covert
  Channels](https://cyberw1ng.medium.com/data-exfiltration-over-dns-http-custom-covert-channels-646d63562c01)
- [What Is DNS Data
  Exfiltration](https://www.akamai.com/glossary/what-is-dns-data-exfiltration)
- [What is DNS
  Tunneling](https://www.paloaltonetworks.ca/cyberpedia/what-is-dns-tunneling)
