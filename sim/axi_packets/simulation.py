import difflib
import logging
import os
import subprocess

# from .axi_lite import get_transactions
from .axi_stream import axis_to_packets, set_globals


NUM_CMAC_PORT = 1
NUM_QDMA = 1
NUM_PHYS_FUNC = 1
NUM_QUEUE = 512
USER_BOX = "__full__"
SIM_LOCATION = os.environ["HOME"]


class SimulationError(Exception):
    pass


class InterfacesManager:

    def __init__(self):
        self.received_packets = dict()
        self.expected_packets = dict()
        self.interfaces = dict()
        self.sim_location = None
        self.box = None

    def _get_interface_names(self):
        for i in range(NUM_CMAC_PORT):
            yield f"phy{i}"
        if self.box == "__250mhz__":
            interfaces_range = NUM_QDMA * NUM_PHYS_FUNC
        # for i in range(interfaces_range):
            # yield f"dma{i}"
        # yield "registers"

    def open_interfaces(self):
        self.box = USER_BOX
        self.sim_location = SIM_LOCATION
        set_globals(self.box, NUM_QUEUE)
        for interface_name in self._get_interface_names():
            self.interfaces[interface_name] = open(f"{self.sim_location}/axi_in_{interface_name}.txt", 'w')
            self.expected_packets[interface_name] = []

    def close_interfaces(self):
        for interface_file in self.interfaces.values():
            interface_file.close()

    def _get_interface(self, name):
        if name not in self.interfaces.keys():
            log.error(f"Invalid interface name {name}")
            return
        return self.interfaces[name]

    def add_sent_packets(self, name, text):
        file = self._get_interface(name)
        if file:
            file.write(text)

    # def add_expected_packets(self, name, packets):
    #     file = self._get_interface(name)
    #     if file:
    #         self.expected_packets[name].extend(packets)

    # def add_received_packets(self):
    #     for interface_name in self._get_interface_names():
    #         file = open(f"{self.sim_location}/axi_out_{interface_name}.txt", 'r')
    #         if interface_name == "registers":
    #             packets = get_transactions(file)
    #         else:
    #             packets = axis_to_packets(file, interface_name)
    #         self.received_packets[interface_name] = packets
    #         file.close()

    # @staticmethod
    # def _compare_packet_lists(received_packets, expected_packets, interface_name=None):
    #     differ = difflib.Differ()
    #     correct = True
    #     for received, expected in zip(received_packets, expected_packets):
    #         if interface_name:
    #             received = received.show2(dump = True)
    #             expected = expected.show2(dump = True)
    #         if received == expected:
    #             continue
    #         correct = False
    #         difference = list(differ.compare(received.splitlines(), expected.splitlines()))
    #         difference_string = '\n'.join(difference)
    #         if interface_name:
    #             log.warning(f"Packet mismatch for {interface_name}:\n{difference_string}")
    #         else:
    #             log.warning(f"Register mismatch:\n{difference_string}")

    #     difference = len(received_packets) - len(expected_packets)
    #     if interface_name and difference != 0:
    #         if difference > 0:
    #             log.warning(f"Received {difference} more packets than expected for interface {interface_name}")
    #         elif difference < 0:
    #             log.warning(f"Expected {-difference} more packet than received from interface {interface_name}")
    #     return correct

    # def compare_packets(self):
    #     packets_correct = True
    #     for interface_name in self._get_interface_names():
    #         expected_packets = self.expected_packets[interface_name]
    #         if not expected_packets or interface_name == "registers":
    #             continue
    #         received_values = self.received_packets[interface_name]
    #         result = self._compare_packet_lists(received_values, expected_packets, interface_name = interface_name)
    #         packets_correct = packets_correct and result
    #     if packets_correct:
    #         log.info("All packets were as expected")

    #     expected_values = self.expected_packets["registers"]
    #     if expected_values:
    #         received_values = self.received_packets["registers"]
    #         if self._compare_packet_lists(received_values, expected_values):
    #             log.info("All register values were as expected")

interface_manager = InterfacesManager()
