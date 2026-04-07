from __future__ import annotations

from . import __name__

from ir.symbols import Symbol
from ir.types import DataType, TensorType
from ir.device import DeviceModel
from ir.placement import Tile, Placement
from ir.kernel import Kernel
from ir.fifo import ObjectFifo, ObjectFifoEndpoint
from ir.worker import Worker
from ir.program import Program


def dtype(name: str) -> DataType:
    return DataType(name)

def tensor(shape: tuple[int, ...], dtype_name: str) -> TensorType:
    return TensorType(shape=shape, dtype=DataType(dtype_name))

def fifo_endpoint(fifo: ObjectFifo, port: str) -> ObjectFifoEndpoint:
    if fifo is None:
        raise ValueError("fifo_endpoint() received fifo=None")
    return ObjectFifoEndpoint(fifo=fifo, port=port)


class ProgramBuilder:
    """
        The frontend builder that changes Python calls into semantic IR
    """
    def __init__(self, device_kind: str) -> None:
        self.program = Program(device=DeviceModel.from_kind(device_kind))
        
    def tile(self, name: str, col:int, row:int, kind: str = "any") -> Tile:
        tile = Tile(sym=Symbol(name), col=col, row=row, kind=kind)
        self.program.add_tile(tile)
        return tile
    
    def kernel(self, name: str, source_file: str, arg_types: list[TensorType], ) -> Kernel:
        kernel = Kernel(sym=Symbol(name), source_file=source_file, arg_types=arg_types)
        self.program.add_kernel(kernel)
        return kernel
    
    def object_fifo(self, name:str, producer: Tile, consumers: list[Tile], 
                    depth: int, elem_type: TensorType,) -> ObjectFifo:
        fifo = ObjectFifo(sym=Symbol(name), producer=producer, consumers=consumers, depth=depth, elem_type=elem_type)
        self.program.add_fifo(fifo)
        return fifo
    
    def worker(self, name: str, tile: Tile)-> Worker:
        worker = Worker(sym=Symbol(name),placement=Placement(tile))
        self.program.add_worker(worker)
        return worker
    
    def build(self) -> Program:
        return self.program
    
        
