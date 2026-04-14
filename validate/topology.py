from ir.program import Program
from ir.worker import KernelCallOp, LoopOp


def _tile_names(program: Program) -> set[str]:
    return {t.name for t in program.tiles}


def _kernel_names(program: Program) -> set[str]:
    return {k.name for k in program.kernels}

def _fifo_names(program: Program) -> set[str]:
    return {f.name for f in program.fifos}


def _validate_worker_ops(worker, kernel_names: set[str]) -> None:
    for op in worker.body:
        if isinstance(op, KernelCallOp):
            if op.kernel.name not in kernel_names:
                raise ValueError(
                    f"Worker '{worker.name}' calls unknown kernel '{op.kernel.name}'"
                )
        elif isinstance(op, LoopOp):
            _validate_loop_body(worker.name, op, kernel_names)


def _validate_loop_body(worker_name: str, loop_op: LoopOp, kernel_names: set[str]) -> None:
    for op in loop_op.body:
        if isinstance(op, KernelCallOp):
            if op.kernel.name not in kernel_names:
                raise ValueError(
                    f"Worker '{worker_name}' loop calls unknown kernel '{op.kernel.name}'"
                )
        elif isinstance(op, LoopOp):
            _validate_loop_body(worker_name, op, kernel_names)


def validate_topology(program: Program) -> None:
    tile_names = _tile_names(program)
    kernel_names = _kernel_names(program)
    fifo_names = _fifo_names(program)

    for fifo in program.fifos:
        if fifo.producer.name not in tile_names:
            raise ValueError(
                f"FIFO '{fifo.name}' producer tile '{fifo.producer.name}' is not in program.tiles"
            )
        for consumer in fifo.consumers:
            if consumer.name not in tile_names:
                raise ValueError(
                    f"FIFO '{fifo.name}' consumer tile '{consumer.name}' is not in program.tiles"
                )
        
    for link in program.fifo_links:
        if link.src.name not in fifo_names:
            raise ValueError(
                f"FIFO link '{link.name}' references unknown source FIFO '{link.src.name}'"
            )
        if link.dst.name not in fifo_names:
            raise ValueError(
                f"FIFO link '{link.name}' references unknown destination FIFO '{link.dst.name}'"
            )

    for worker in program.workers:
        placed_tile = worker.placement.tile
        if placed_tile.name not in tile_names:
            raise ValueError(
                f"Worker '{worker.name}' is placed on unknown tile '{placed_tile.name}'"
            )
        _validate_worker_ops(worker, kernel_names)