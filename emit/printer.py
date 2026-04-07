class Printer:
    """
        Small Printer class for MLIR emission
    """
    def __init__(self, indent_unit: str = "  ") -> None:
        self._lines: list[str] = []
        self._level: int = 0
        self._indent_unit = indent_unit
    
    def writeln(self, line: str = "") -> None:
        self._lines.append(f"{self._indent_unit * self._level}{line}")
        
    def indent(self) -> None:
        self._level += 1
    
    def dedent(self) -> None:
        if self._level == 0:
            raise ValueError("Cannot dedent below zero")
        self._level -= 1
        
    def getvalue(self) -> str:
        return "\n".join(self._lines) + "\n"