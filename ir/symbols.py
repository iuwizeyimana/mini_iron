from dataclasses import dataclass

@dataclass
class Symbol:
    """
        Represents a symbol name
        e.g: "core0", "in_fifo", "matmul_bf16"
    """
    
    name: str
    
    def __post_init(self) -> None:
        if not self.name:
            raise ValueError("Symbol name cannot be empty")
        if " " in self.name:
            raise ValueError("Symbol name cannot contain spaces: {self.name}")
        
    def __str__(self) -> str:
        return self.name