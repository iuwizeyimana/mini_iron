from dataclasses import dataclass

from .fifo import ObjectFifo
from .symbols import Symbol


@dataclass
class FifoLink:
    """
    Logical connection between two FIFOs.
    """
    sym: Symbol
    src: ObjectFifo
    dst: ObjectFifo

    @property
    def name(self) -> str:
        return self.sym.name