from dataclasses import dataclass, field
from typing import List, Optional
from .device import DeviceModel
from .placement import Tile
from .kernel import Kernel
from .fifo import ObjectFifo
from .worker import Worker
from .runtime import RuntimeSequence

@dataclass
class Program:
    """
    Top - level semantic IR 
    """
    
    device: DeviceModel
    tiles: List[Tile] = field(default_factory=list)
    kernels: List[Kernel] = field(default_factory=list)
    fifos: List[ObjectFifo] = field(default_factory=list)
    workers: List[Worker] = field(default_factory=list)
    runtime_sequences: List[RuntimeSequence] = field(default_factory=list)
    
    
    def add_tile(self, tile: Tile) -> None:
        self.tiles.append(tile)
    
    def add_kernel(self, kernel: Kernel) -> None:
        self.kernels.append(kernel)
    
    def add_fifo(self, fifo: ObjectFifo) -> None:
        self.fifos.append(fifo)
        
    def add_worker(self, worker: Worker) -> None:
        self.workers.append(worker)
        
    def add_runtime_sequence(self, seq: RuntimeSequence) -> None:
        self.runtime_sequences.append(seq)
        
    def find_tile(self, name: str) -> Optional[Tile]:
        for tile in self.tiles:
            if tile.name == name:
                return tile
        return None
    
    def find_kernel(self, name: str) -> Optional[Kernel]:
        for kernel in self.kernels:
            if kernel.name == name:
                return kernel
        return None
    
    def find_fifo(self, name: str) -> Optional[ObjectFifo]:
        for fifo in self.fifos:
            if fifo.name == name:
                return fifo
        return None
    
    def find_worker(self, name: str) -> Optional[Worker]:
        for worker in self.workers:
            if worker.name == name:
                return worker
        return None
    
    def find_runtime_sequence(self, name: str) -> Optional[RuntimeSequence]:
        for seq in self.runtime_sequences:
            if seq.name == name:
                return seq
        return None