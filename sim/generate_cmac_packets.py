import axi_packets

src_mac = "00:11:22:33:44:55"
dst_mac = "55:44:33:22:11:00"

src_ip = "1.2.3.4"
dst_ip = "4.3.2.1"

PAYLOAD_SIZE = 1024 - 4 - 8
payload = bytes.fromhex("deadbeef") * (PAYLOAD_SIZE // 4)
# payload = payload[:PAYLOAD_SIZE]

opcode = 1  # Write
key = 25
write_packet = axi_packets.make_replication_packet(dst_mac=dst_mac, src_mac=src_mac, dst_ip=dst_ip, src_ip=src_ip, opcode=opcode, key=key, payload=payload)

opcode = 0  # Read
read_packet = axi_packets.make_replication_packet(dst_mac=dst_mac, src_mac=src_mac, dst_ip=dst_ip, src_ip=src_ip, opcode=opcode, key=key, payload="")

axi_packets.interface_manager.open_interfaces()
axi_packets.send_packets("cmac0", write_packet)
axi_packets.make_cycles_delay("cmac0", 1000)
axi_packets.send_packets("cmac0", read_packet)
axi_packets.interface_manager.close_interfaces()

