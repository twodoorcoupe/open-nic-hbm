# OpenNIC HBM
This project adds High Bandwidth Memory (HBM) to OpenNIC. 
Also, it provides a testbench to simulate PCIe between host and QDMA and a Python API to feed packets to CMAC. 

The [replication branch](https://github.com/twodoorcoupe/open-nic-hbm/tree/replication) adds a data replication protocol that uses the HBM, and a leader election mechanism.

## Requirements
### Hardware
This project is intended for the Alveo U55C card.
But, after modification to the [build script](https://github.com/twodoorcoupe/open-nic-hbm/blob/main/build.tcl), it should work for any Alveo card with HBM, such as:
- Xilinx Alveo U50
- Xilinx Alveo U55C
- Xilinx Alveo 280
- Xilinx Alveo V80

### Software
The project was built with Vivado 2024.2. But, to use other Vivado versions, the only thing that would need to be modified would be the block diagram located at `open-nic-shel/src/hbm_subsystem/hbm_bd.tcl`.

The simulation uses Questa simulator by default, but one could modify the project's settings to use any simulator they wish, including Vivado's own.
Remember that to use an external simulator, Vivado needs to [compile the simulation libraries](https://docs.amd.com/r/en-US/ug892-vivado-design-flows-overview/Compiling-Simulation-Libraries).

## Repo Structure


## How to Build
1. Clone the repo and update the OpenNIC shell submodule
```
git clone https://github.com/twodoorcoupe/open-nic-hbm.git
cd open-nic-hbm
git submodule update --init --recursive
```
2. Apply the patch to OpenNIC
```
cd open-nic-shell
git apply ../patches/open_nic_hbm.patch
cd ..
```
3. Source Vivado and run build script
```
source /tools/Xilinx/Vivado/2024.2/settings64.sh
vivado -mode batch -source build.tcl
```

## Simulation

