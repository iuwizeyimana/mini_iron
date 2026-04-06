from dataclasses import dataclass, field
from typing import List, Optional
from .symbols import Symbol
from .placement import Placement
from .fifo import ObjectFifoEndpoint
from .kernel import Kernel

@dataclass
class WorkerOp:
    """
        Base class for worker
    """

@dataclass
class AcquireOp(WorkerOp):
    endpoint: ObjectFifoEndpoint
    count: int = 1
    alias: Optional[str] = None
    
    def __post_init__(self) -> None:
        if self.count <= 0:
            raise ValueError(f"AcquireOp count must be > 0 , got {self.count}")
    

@dataclass
class ReleaseOp(WorkerOp):
    endpoint: ObjectFifoEndpoint
    count: int = 1
    
    def __post_init__(self) -> None:
        if self.count <= 0:
            raise ValueError(f"ReleaseOp count must be >0, got {self.count}")

@dataclass
class KernelCallOp(WorkerOp):
    """
        describes kernel call, e.g: matmul(elem_in_x, elem_in_y, elem_out)
    """
    
    kernel: Kernel
    operands: List[str] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        if len(self.operands) != self.kernel.arity():
            raise ValueError(
                f"KernelCallOp operand count mismatch for '{self.kernel.name}': "
                f"expected {self.kernel.arity()}, got {len(self.operands)}"
            )

@dataclass 
class LoopOp(WorkerOp):
    """
    """
    
    body: List[WorkerOp] = field(default_factory=list)
    trip_count: Optional[int] = None
    
    def __post_init__(self) -> None:
        if self.trip_count is not None and self.trip_count <= 0:
            raise ValueError(f"LoopOp trip_count must be > 0, got {self.trip_count}")
        

@dataclass
class Worker:
    """
        Represents the program running on one compute tile
    """
    sym: Symbol
    placement: Placement
    body: List[WorkerOp] = field(default_factory=list)
    
    @property 
    def name(self) -> str:
        return self.sym.name
    def add_op(self, op: WorkerOp) -> None:
        self.body.append(op)
        
    def acquire(
        self, 
        endpoint: ObjectFifoEndpoint, 
        count: int = 1,
        alias: Optional[str] = None,
    ) -> None:
        self.add_op(AcquireOp(endpoint=endpoint, count=count, alias=alias))
        
    def release(self, endpoint: ObjectFifoEndpoint, count: int = 1) -> None:
        self.add_op(ReleaseOp(endpoint=endpoint, count=count))
        
    def call(self, kernel: Kernel, operands: List[str]) -> None:
        self.add_op(KernelCallOp(kernel=kernel, operands=operands))
        
    def loop(self, body: List[WorkerOp], trip_count: Optional[int] = None) -> None:
        self.add_op(LoopOp(body=body, trip_count=trip_count))
    
    
    
    