from dataclasses import dataclass, field
from typing import List
from .symbols import Symbol
from .types import TensorType
from .placement import Tile

@dataclass
class ObjectFifo:
    """
        Similar to IRON, these are FIFO channels that coonect tiles
        
        producer: one source tile
        consumers: destination tiles (could be one or more)
        depth: object FIFO depth (depth or 2 is used to compute-communication overlap)
        elem_type: the TensorType of each object
    """
    sym: Symbol
    producer: Tile
    consumers: List[Tile]
    depth: int
    elem_type: TensorType
    
    def __post_init__(self) -> None:
        if self.depth <= 0:
            raise ValueError(f"ObjectFifo depth must be > 0, got {self.depth}")
        
        if not self.consumers:
            raise ValueError("ObjectFifo must have at least one consumer")
        
    @property
    def name(self) -> str:
        return self.sym.name

@dataclass
class ObjectFifoEndpoint:
    """
        Object FIFO endpoint usee from the pov of a worker op
        
        port: Produce or Consume
    """
    
    fifo: ObjectFifo
    port: str
    
    def __post_init__(self) -> None:
        if self.port not in ("Produce", "Consume"):
            raise ValueError(f"Invalid FIFO port: {self.port}")
        
    @property
    def name(self) -> str:
        return f"{self.fifo.name}:{self.port}"
    
        
    
        
    