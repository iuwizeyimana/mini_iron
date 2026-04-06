from dataclasses import dataclass
from typing import Tuple

@dataclass
class DataType:
    """
        Supported scalar data types
        e.g.: "i16" for int16, "bf16" for bflooat16
    """
    name: str
    # only supports a fixed set of dtypes
    _SUPPORTED = {"i8", "i16", "i32", "i64", "bf16", "f16", "f32"}
    
    def __post_init__(self) -> None:
        if self.name not in self._SUPPORTED:
            raise ValueError(
                f"Unsupported dtype '{self.name}'. Supported: {sorted(self._SUPPORTED)}"
            )
    def __str__(self) -> str:
        return self.name
    
@dataclass
class TensorType:
    """
        Tensor memref-like type; should have shape and dtype
        e.g: memref<64x64xi16> being a tensor of shape (64x64) and int16 dtype 
    """
    shape: Tuple[int, ...]
    dtype: DataType
    
    def __post_init__(self) -> None:
        if not self.shape:
            raise ValueError("TensorType shape cannot be empty")
        if any(d <= 0 for d in self.shape):
            raise ValueError(f"All TensorType dimensions must be > 0 , got {self.shape}")
        
    def rank(self) -> int:
        return len(self.shape)
    
    def num_elements(self) -> int:
        total = 1
        for d in self.shape:
            total *= d
        return total
    
    def to_memref_str(self) -> str:
        dims = "x".join(str(d) for d in self.shape)
        return  f"memref{dims}x{self.dtype}"
    
    def __str__(self) -> str:
        dims = "x".join(str(d) for d in self.shape)
        return f"{dims}x{self.dtype}"
    
    
    