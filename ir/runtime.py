from dataclasses import dataclass, field
from typing import List

from .symbols import Symbol
from .fifo import ObjectFifo
from .worker import Worker

@dataclass
class RuntimeOp:
    """
        Base class for runtime/orchestration operations
    """
    
@dataclass
class HostToFifoOp(RuntimeOp):
    """
        Move data from a host buffer into an input FIFO
    """
    
    fifo: ObjectFifo
    host_buffer_name: str
    
    def __post_init__(self) -> None:
        if not self.host_buffer_name:
            raise ValueError("HostToFifoOp host_buffer_name cannot be empty")
    

@dataclass
class FifoToHostOp(RuntimeOp):
    """
        Move data from a output FIFO to a host buffer
    """
    fifo: ObjectFifo
    host_buffer_name: str
    
    def __post_init__(self) -> None:
        if not self.host_buffer_name:
            raise ValueError("FifoToHostOp host_buffer_name cannot be empty")
        
@dataclass 
class StartWorkersOp(RuntimeOp):
    workers: List[Worker] = field(default_factory=list)
    
    def __post_init_(self) -> None:
        if not self.workers:
            self.ValueError("StartWorkersOp requires at least one worker")

@dataclass
class AwaitWorkersOp(RuntimeOp):
    """
    Wait for one or more workers to complete.
    """
    workers: List[Worker] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.workers:
            raise ValueError("AwaitWorkersOp requires at least one worker")


@dataclass
class RuntimeSequence:
    """
    Top-level runtime sequence for host/AIE orchestration.
    """
    sym: Symbol
    ops: List[RuntimeOp] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.sym.name

    def add_op(self, op: RuntimeOp) -> None:
        self.ops.append(op)

    def host_to_fifo(self, fifo: ObjectFifo, host_buffer_name: str) -> None:
        self.add_op(HostToFifoOp(fifo=fifo, host_buffer_name=host_buffer_name))

    def fifo_to_host(self, fifo: ObjectFifo, host_buffer_name: str) -> None:
        self.add_op(FifoToHostOp(fifo=fifo, host_buffer_name=host_buffer_name))

    def start(self, workers: List[Worker]) -> None:
        self.add_op(StartWorkersOp(workers=workers))

    def await_workers(self, workers: List[Worker]) -> None:
        self.add_op(AwaitWorkersOp(workers=workers))
    