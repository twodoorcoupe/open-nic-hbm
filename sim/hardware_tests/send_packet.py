from scapy.all import sendp, sniff
import argparse
import axi_packets
import threading
import time

iface = "enp7s0"
src_mac = "02:0a:35:00:07:00"
dst_mac = "02:0a:35:07:00:00"
src_ip = "192.100.51.0"
dst_ip = "192.100.51.1"

payload_size = 1024 - 4 - 8
default_payload = bytes.fromhex("dead0000") * (payload_size // 4)
ignored_names = {6, 8}
opcode_map = {
    "read": {"code": 0, "payload": b""},
    "write": {"code": 1, "payload": default_payload},
    "write_ack": {"code": 4, "payload": b""},
    "write_leader": {"code": 2, "payload": default_payload},
    "heartbeat": {"code": 6, "payload": b""},
    "heartbeat_ack": {"code": 7, "payload": b""},
    "vote_request": {"code": 8, "payload": b""},
    "vote": {"code": 9, "payload": b""}
}

parser = argparse.ArgumentParser()
parser.add_argument("opcode", choices=list(opcode_map.keys()))
parser.add_argument("key", type=int, default=0)
parser.add_argument("--id", "-i", type=int, default=1)
args = parser.parse_args()

if args.opcode not in opcode_map:
    raise SystemExit(f"Unsupported opcode: {args.opcode}")

mapping = opcode_map[args.opcode]
opcode = mapping["code"]
key = args.key
packet_id = args.id
payload = mapping.get("payload", b"")

packet = axi_packets.make_replication_packet(
    dst_mac=dst_mac,
    src_mac=src_mac,
    dst_ip=dst_ip,
    src_ip=src_ip,
    opcode=opcode,
    key=key,
    id=packet_id,
    payload=payload
)

def keep_packet(pkt):
    op = pkt["Replication"].opcode
    if op in ignored_names:
        return False
    return True

def sniff_response():
    response = sniff(count=2, iface=iface, lfilter=keep_packet, timeout=5)
    for p in response:
        p.show()

sniff_thread = threading.Thread(target=sniff_response)
sniff_thread.start()
time.sleep(0.1)
sendp(packet, iface=iface, count=1, verbose=True)
sniff_thread.join()
