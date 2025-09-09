#!/usr/bin/env python3
from scapy.all import Packet, bind_layers, ByteField, BitField, Raw, Ether, IP, UDP

class Replication(Packet):
  name = "Replication"
  fields_desc = [
    ByteField("opcode", 0),
    ByteField("id", 0),
    BitField("key", 0, 64),
  ]

bind_layers(UDP, Replication, dport=30583)
bind_layers(Replication, Raw)

def make_replication_packet(dst_mac, src_mac, dst_ip, src_ip, opcode, key, payload):
  eth = Ether(dst=dst_mac, src=src_mac)
  ip = IP(dst=dst_ip, src=src_ip)
  udp = UDP(sport=30583, dport=30583)
  rep = Replication(opcode=opcode, id=0, key=key)
  pkt = eth / ip / udp / rep / Raw(payload)
  return pkt
