from ir.program import Program
from ir.worker import AcquireOp, ReleaseOp, KernelCallOp, LoopOp
from .printer import Printer
from .mlir_types import emit_memref_type
from .emit_aiex import emit_aiex_runtime_block


def _device_attr(kind: str) -> str:
    mapping = {
        "npu1_1col": "AIEDevice.npu1_1col",
        "npu2": "AIEDevice.npu2",
    }
    if kind not in mapping:
        raise ValueError(f"Unsupported device kind for MLIR emission: {kind}")
    return mapping[kind]


def _tile_ssa_name(tile_name: str) -> str:
    return f"%tile_{tile_name}"


def _emit_kernel_decl(printer: Printer, kernel) -> None:
    arg_str = ", ".join(emit_memref_type(arg) for arg in kernel.arg_types)
    printer.writeln(f"aie.external_func @{kernel.name}({arg_str})")


def _emit_fifo_decl(printer: Printer, fifo) -> None:
    producer = _tile_ssa_name(fifo.producer.name)
    if len(fifo.consumers) == 1:
        consumers = _tile_ssa_name(fifo.consumers[0].name)
    else:
        consumers = "[" + ", ".join(_tile_ssa_name(t.name) for t in fifo.consumers) + "]"

    elem_type = emit_memref_type(fifo.elem_type)
    printer.writeln(
        f'aie.object_fifo @{fifo.name}({producer}, {consumers}, {fifo.depth} : {elem_type})'
    )

def _emit_fifo_link_decl(printer: Printer, link) -> None:
    printer.writeln(f"aie.object_fifo_link @{link.name}(@{link.src.name}, @{link.dst.name})")


def _emit_worker_op(printer: Printer, op, loop_depth: int = 0) -> None:
    if isinstance(op, AcquireOp):
        alias = f" as {op.alias}" if op.alias else ""
        printer.writeln(
            f"// acquire {op.endpoint.fifo.name} {op.endpoint.port} {op.count}{alias}"
        )
    elif isinstance(op, ReleaseOp):
        printer.writeln(
            f"// release {op.endpoint.fifo.name} {op.endpoint.port} {op.count}"
        )
    elif isinstance(op, KernelCallOp):
        operands = ", ".join(op.operands)
        printer.writeln(f"// call @{op.kernel.name}({operands})")
    elif isinstance(op, LoopOp):
        if op.trip_count is None:
            printer.writeln("// loop forever {")
        else:
            printer.writeln(f"// loop {op.trip_count} times {{")
        printer.indent()
        for nested in op.body:
            _emit_worker_op(printer, nested, loop_depth + 1)
        printer.dedent()
        printer.writeln("// }")
    else:
        raise TypeError(f"Unsupported worker op for emission: {type(op).__name__}")


def _emit_core(printer: Printer, worker) -> None:
    tile_name = _tile_ssa_name(worker.placement.tile.name)
    printer.writeln(f"aie.core({tile_name}) {{")
    printer.indent()

    for op in worker.body:
        _emit_worker_op(printer, op)

    printer.writeln("aie.end")
    printer.dedent()
    printer.writeln("}")


def emit_aie_module(program: Program) -> str:
    printer = Printer()

    printer.writeln("module {")
    printer.indent()

    printer.writeln(f"aie.device({_device_attr(program.device.kind)}) {{")
    printer.indent()

    for tile in program.tiles:
        printer.writeln(
            f"{_tile_ssa_name(tile.name)} = aie.tile({tile.col}, {tile.row})"
        )

    if program.tiles:
        printer.writeln()

    for kernel in program.kernels:
        _emit_kernel_decl(printer, kernel)

    if program.kernels:
        printer.writeln()

    for fifo in program.fifos:
        _emit_fifo_decl(printer, fifo)

    if program.fifos:
        printer.writeln()
    
    for link in program.fifo_links:
        _emit_fifo_link_decl(printer, link)

    if program.fifo_links:
        printer.writeln()

    for worker in program.workers:
        _emit_core(printer, worker)
        printer.writeln()

    printer.dedent()
    printer.writeln("}")
    
    runtime_text = emit_aiex_runtime_block(program)
    if runtime_text.strip():
        for line in runtime_text.rstrip("\n").split("\n"):
            printer.writeln(line)

    printer.dedent()
    printer.writeln("}")

    return printer.getvalue()