from scapy.all import sendp, sniff
import argparse
import axi_packets
import threading
import time

iface = "enp7s0"
src_mac = "02:0a:35:00:07:00"
dst_mac = "02:0a:35:07:00:00"

src_ip = "192.100.52.1"
dst_ip = "192.100.51.1"

PAYLOAD_SIZE = 1024 - 4 - 8
payload = bytes.fromhex("dead0000") * (PAYLOAD_SIZE // 4)

opcode = 0
key = 5475743975987432997
id = 10


parser = argparse.ArgumentParser()
parser.add_argument("opcode", choices=["read", "write", "write_ack", "write_leader", "normal"])
parser.add_argument("key")
args = parser.parse_args()

key = int(args.key)
if args.opcode == "read":
    opcode = 0
    payload = ""
elif args.opcode == "write":
    opcode = 1
elif args.opcode == "write_ack":
    opcode = 3
    payload = ""
    key = 10000
    id = 5
elif args.opcode == "write_leader":
    opcode = 1
    key = 10000
    

if args.opcode == "normal":
    packet = axi_packets.make_ip_pkt(
        pkt_len=PAYLOAD_SIZE,
        dst_mac=dst_mac, 
        src_mac=src_mac, 
        dst_ip=dst_ip, 
        src_ip=src_ip, 
    )   
    sendp(packet, iface=iface, count =1, verbose=True)
else:
    packet = axi_packets.make_replication_packet(
        dst_mac=dst_mac, 
        src_mac=src_mac, 
        dst_ip=dst_ip, 
        src_ip=src_ip, 
        opcode=opcode, 
        key=key, 
      	id=id,
        payload=payload
    )

    print(opcode)
    print(key)
    print(packet)

    def sniff_response():
        response = sniff(count=2, iface=iface)
        response[0].show()
        response[1].show()

    sniff_thread = threading.Thread(target=sniff_response)
    sniff_thread.start()
    time.sleep(1)
    sendp(packet, iface=iface, count =1, verbose=True)
    sniff_thread.join()
