# Script to send replication packets to NIC
from scapy.all import sendp
import argparse
import axi_packets

iface = "enp7s0"
src_mac = "02:0a:35:07:00:00"
dst_mac = "02:0a:35:00:07:00"

src_ip = "192.100.51.1"
dst_ip = "192.100.52.1"

PAYLOAD_SIZE = 1024 - 4 - 8
payload = bytes.fromhex("deadbeef") * (PAYLOAD_SIZE // 4)

opcode = 0
key = 1


parser = argparse.ArgumentParser()
parser.add_argument("opcode", choices=["read", "write", "write_ack", "write_leader", "normal"])
args = parser.parse_args()

if args.opcode == "read":
    opcode = 0
elif args.opcode == "write":
    opcode = 1
elif args.opcode == "write_ack":
    opcode = 3
elif args.opcode == "write_leader":
    opcode = 1
    key = 0

packet = axi_packets.make_replication_packet(
	dst_mac=dst_mac, 
	src_mac=src_mac, 
	dst_ip=dst_ip, 
	src_ip=src_ip, 
	opcode=opcode, 
	key=key, 
	payload=payload
)
    
if args.opcode == "normal":
    packet = axi_packets.make_ip_pkt(
    	dst_mac=dst_mac, 
	src_mac=src_mac, 
	dst_ip=dst_ip, 
	src_ip=src_ip, 
    )

sendp(packet,iface=iface, count =1 , verbose=True)
