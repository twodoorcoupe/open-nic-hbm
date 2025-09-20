#!/usr/bin/env python3
from scapy.all import sniff, Ether, IP, UDP, Raw, sendp
import axi_packets
import threading
import time


iface = "enp7s0"

MEMORY_SIZE = 100
CHUNK_SIZE = 1024
memory = [bytearray(CHUNK_SIZE) for _ in range(MEMORY_SIZE)]
running = threading.Event()
running.set()


def enqueue_packet(pkt):
  if (pkt.haslayer(Ether) and pkt.haslayer(IP) and pkt.haslayer(UDP)):
    print('Caught UDP packet')

  if not (pkt.haslayer(Ether) and pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(axi_packets.Replication)):
    return
  
  print('Caught replication packet')
  src_mac = pkt[Ether].dst
  dst_mac = pkt[Ether].src
  src_ip = pkt[IP].dst
  dst_ip = pkt[IP].src
  resp = axi_packets.make_ip_pkt(dst_mac=src_mac, src_mac=dst_mac, dst_ip=src_ip, src_ip=dst_ip)

  rep = pkt[axi_packets.Replication]
  key = int(getattr(rep, 'key', 0))
  idx = int(getattr(rep, 'idx', 0))
  opcode = int(getattr(rep, 'opcode', 0))
  address = key % MEMORY_SIZE

  if opcode == 0:  # Read
    opcode = 2
    data = bytes(memory[address])
    resp = axi_packets.make_replication_packet(dst_mac=src_mac, src_mac=dst_mac, dst_ip=src_ip, src_ip=dst_ip, opcode=opcode, key=key, id=idx, payload=data)
  elif opcode == 1:  # Write
    opcode = 3
    data = pkt[Raw]
    memory[address] = data
    resp = axi_packets.make_replication_packet(dst_mac=src_mac, src_mac=dst_mac, dst_ip=src_ip, src_ip=dst_ip, opcode=opcode, key=key, payload="")

  sendp(resp, iface=iface, verbose=False)


def sniffer():
  sniff(prn=enqueue_packet, iface=iface, store=False)


if __name__ == '__main__':
  sniffer_thread = threading.Thread(target=sniffer, daemon=True)
  sniffer_thread.start()
  try:
    while running.is_set():
      time.sleep(1)
      print('Waiting...')
  except KeyboardInterrupt:
    running.clear()
  sniffer_thread.join()
