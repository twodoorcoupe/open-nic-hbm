import axi_packets

src_mac = "00:11:22:33:44:55"
dst_mac = "55:44:33:22:11:00"

src_ip = "1.2.3.4"
dst_ip = "4.3.2.1"

PAYLOAD_SIZE = 1024 - 4 - 8
payload = bytes.fromhex("deadbeef") * (PAYLOAD_SIZE // 4)

axi_packets.interface_manager.open_interfaces()

key = 25
opcode = 1  # Write
write_packet = axi_packets.make_replication_packet(dst_mac=dst_mac, src_mac=src_mac, dst_ip=dst_ip, src_ip=src_ip, opcode=opcode, key=key, payload=payload)
axi_packets.send_packets("cmac0", write_packet)

axi_packets.make_cycles_delay("cmac0", 1000)

opcode = 0  # Read
read_packet = axi_packets.make_replication_packet(dst_mac=dst_mac, src_mac=src_mac, dst_ip=dst_ip, src_ip=src_ip, opcode=opcode, key=key, payload="")
axi_packets.send_packets("cmac0", read_packet)

axi_packets.make_cycles_delay("cmac0", 1000)

key = 100
id = 100
opcode = 1  # Write to leader
write_packet = axi_packets.make_replication_packet(dst_mac=dst_mac, src_mac=src_mac, dst_ip=dst_ip, src_ip=src_ip, opcode=opcode, key=key, id=id, payload=payload)
axi_packets.send_packets("cmac0", write_packet)

axi_packets.make_cycles_delay("cmac0", 1000)

key = 100
id = 1
opcode = 3  # Write ack
write_packet = axi_packets.make_replication_packet(dst_mac=dst_mac, src_mac=src_mac, dst_ip=dst_ip, src_ip=src_ip, opcode=opcode, key=key, id=id, payload="")
axi_packets.send_packets("cmac0", write_packet)

key = 100
id = 1
opcode = 4  # Write ack from leader
write_packet = axi_packets.make_replication_packet(dst_mac=dst_mac, src_mac=src_mac, dst_ip=dst_ip, src_ip=src_ip, opcode=opcode, key=key, id=id, payload="")
axi_packets.send_packets("cmac0", write_packet)

axi_packets.interface_manager.close_interfaces()

