from ir.program import Program

def _check_unique(kind: str, names: list[str]) -> None:
    seen = set()
    duplicates = []
    for name in names:
        if name in seen:
            duplicates.append(name)
        seen.add(name)
    
    if duplicates:
        dup_str = ", ".join(sorted(set(duplicates)))
        raise ValueError(f"Duplicate {kind} names found: {dup_str}")
    
def validate_unique_names(program: Program) -> None:
    _check_unique("tile", [t.name for t in program.tiles])
    _check_unique("kernel", [k.name for k in program.kernels])
    _check_unique("fifo", [f.name for f in program.fifos])
    _check_unique("worker", [w.name for w in program.workers])
    