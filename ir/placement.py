from dataclasses import dataclass
from .symbols import Symbol

@dataclass
class Tile:
    """
        Physical tile (e.g: compute tile, mem tile, shim tile)
        
        Kind can be "shim", "mem" or "core"
        the Symbol can be anything the user wants to name this thing
        the user must specify which row and columns the tile resides
        
        this is a starter pack -- there must be assert messages to ensure placement matches tile kind
    """
    sym: Symbol
    col: int
    row: int
    kind: str = "any" # shouldn't be any but starter guide
    
    def __post_init__(self) -> None:
        if self.col < 0 or self.row<0:
            raise ValueError(f"Tile coordinates must be non-negative, got ({self.col}, {self.row})")
        
    @property
    def name(self) -> str:
        return self.sym.name
    
    def coord(self) -> tuple[int, int]:
        return (self.col, self.row)
    
@dataclass
class Placement:
    """
        Places an IR object to a tile
    """
    tile: Tile
    
    