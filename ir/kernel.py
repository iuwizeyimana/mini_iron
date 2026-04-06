from dataclasses import dataclass, field
from typing import List
from .symbols import Symbol
from .types import TensorType

@dataclass
class Kernel:
    """
        Represents an external kernel callable from a compute core body
        source_file: path to the C++ kernel source to compile later
        arg_types: argument types this kernel takes (should be validated in future MLIR emissions)
    """
    
    sym: Symbol
    source_file: str
    arg_types: List[TensorType] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        if not self.source_file:
            raise ValueError("Kernel source_file cannot be empty")
        
    @property
    def name(self) -> str:
        return self.sym.name
    
    def arity(self) -> int:
        return len(self.arg_types)
    
    