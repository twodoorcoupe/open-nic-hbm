import axi_packets

packet = axi_packets.make_ip_pkt(128)

axi_packets.interface_manager.open_interfaces()
axi_packets.send_packets("cmac0", packet)
axi_packets.interface_manager.close_interfaces()

