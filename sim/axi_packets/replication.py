#!/usr/bin/env python3
from enum import Enum
from scapy.all import Packet, bind_layers, ByteField, BitField, Raw, Ether, IP, UDP


class Opcode(Enum):
  READ = 0
  WRITE = 1
  READ_RESULT = 2
  WRITE_ACK = 3


class Replication(Packet):
  name = "Replication"
  fields_desc = [
    ByteField("opcode", 0),
    ByteField("id", 0),
    BitField("key", 0, 64),
  ]


def make_replication_packet(dst_mac, src_mac, dst_ip, src_ip, opcode, key, payload, id=0):
  eth = Ether(dst=dst_mac, src=src_mac)
  ip = IP(dst=dst_ip, src=src_ip)
  udp = UDP(sport=30583, dport=30583)
  rep = Replication(opcode=opcode, id=id, key=key)
  pkt = eth / ip / udp / rep / Raw(payload)
  return pkt


bind_layers(UDP, Replication, dport=30583)
bind_layers(Replication, Raw)
