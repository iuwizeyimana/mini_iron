from ir.program import Program
from ir.runtime import  HostToFifoOp, FifoToHostOp, StartWorkersOp, AwaitWorkersOp


def _fifo_names(program: Program) -> set[str]:
    return {f.name for f in program.fifos}


def _worker_names(program: Program) -> set[str]:
    return {w.name for w in program.workers}


def validate_runtime(program: Program) -> None:
    """
    Validate runtime/orchestration sequences.

    Current checks:
      - referenced FIFOs exist in the program
      - referenced workers exist in the program
      - host buffer names are non-empty
    """
    fifo_names = _fifo_names(program)
    worker_names = _worker_names(program)

    for seq in program.runtime_sequences:
        for op in seq.ops:
            if isinstance(op, HostToFifoOp):
                if op.fifo.name not in fifo_names:
                    raise ValueError(
                        f"Runtime sequence '{seq.name}' references unknown FIFO "
                        f"'{op.fifo.name}' in HostToFifoOp"
                    )
                if not op.host_buffer_name:
                    raise ValueError(
                        f"Runtime sequence '{seq.name}' has empty host buffer name "
                        f"in HostToFifoOp"
                    )

            elif isinstance(op, FifoToHostOp):
                if op.fifo.name not in fifo_names:
                    raise ValueError(
                        f"Runtime sequence '{seq.name}' references unknown FIFO "
                        f"'{op.fifo.name}' in FifoToHostOp"
                    )
                if not op.host_buffer_name:
                    raise ValueError(
                        f"Runtime sequence '{seq.name}' has empty host buffer name "
                        f"in FifoToHostOp"
                    )

            elif isinstance(op, StartWorkersOp):
                for worker in op.workers:
                    if worker.name not in worker_names:
                        raise ValueError(
                            f"Runtime sequence '{seq.name}' references unknown worker "
                            f"'{worker.name}' in StartWorkersOp"
                        )

            elif isinstance(op, AwaitWorkersOp):
                for worker in op.workers:
                    if worker.name not in worker_names:
                        raise ValueError(
                            f"Runtime sequence '{seq.name}' references unknown worker "
                            f"'{worker.name}' in AwaitWorkersOp"
                        )

            else:
                raise TypeError(
                    f"Unsupported runtime op in validation: {type(op).__name__}"
                )