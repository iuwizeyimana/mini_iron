# mini_iron
Educational toolkit inspired by MLIR-AIE IRON to understand the using MLIR for HW description


[MLIR AIE](https://github.com/Xilinx/mlir-aie) is an [IREE](https://github.com/iree-org/iree) inspired MLIR toolchain used to program AMD's XDNA NPUs.


The NPU is made up of a set of compute tiles, memory tiles that serves a scratchpad, and DMA engines that are called shim tiles. 

The NPU compute tiles are programmed by writting dedicated C++ kernel that use AMD's AIE library to specify vector or scalar computations. 

**IRON** is a Python API that can be used to describe kernel-to-core placement and explicitly scheduled data movement within the NPU. 

An example of using IRON to program the NPU can be seen [here](https://github.com/iuwizeyimana/GRU_on_NPU). 

IRON can be thought of as MLIR-AIE's python front end; its source code can be found [here](https://github.com/Xilinx/mlir-aie/tree/main/python/iron). 
The frontend is used to create MLIR-AIE intermediate representation which undergo a further IR lowering, placement and routing passes and are finally converted into a set of binaries that are used to configure and program the NPU.


The source code is quite developed which unfortunately means it take time to comprehend, hence why I am creating this small, simplified toolkit that mimic's IRON's python frontend. 

