import nictest

packet = nictest.make_ip_pkt(128)

nictest.interface_manager.open_interfaces()
nictest.send_packets("phy0", packet)
nictest.interface_manager.close_interfaces()

