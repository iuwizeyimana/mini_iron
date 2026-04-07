from ir.program import Program
from ir.runtime import  HostToFifoOp, FifoToHostOp, StartWorkersOp, AwaitWorkersOp

from .printer import Printer


def _emit_runtime_op(printer: Printer, op) -> None:
    if isinstance(op, HostToFifoOp):
        printer.writeln(
            f"// runtime: host -> fifo @{op.fifo.name} from %{op.host_buffer_name}"
        )
    elif isinstance(op, FifoToHostOp):
        printer.writeln(
            f"// runtime: fifo @{op.fifo.name} -> host %{op.host_buffer_name}"
        )
    elif isinstance(op, StartWorkersOp):
        names = ", ".join(w.name for w in op.workers)
        printer.writeln(f"// runtime: start workers [{names}]")
    elif isinstance(op, AwaitWorkersOp):
        names = ", ".join(w.name for w in op.workers)
        printer.writeln(f"// runtime: await workers [{names}]")
    else:
        raise TypeError(f"Unsupported runtime op for emission: {type(op).__name__}")


def emit_aiex_runtime_block(program: Program) -> str:
    """
    Emit a very small AIEX-like runtime section.
    """
    if not program.runtime_sequences:
        return ""

    printer = Printer()
    for seq in program.runtime_sequences:
        printer.writeln(f"// ---- runtime sequence: {seq.name} ----")
        printer.writeln(f"func.func @{seq.name}() {{")
        printer.indent()
        for op in seq.ops:
            _emit_runtime_op(printer, op)
        printer.writeln("return")
        printer.dedent()
        printer.writeln("}")
        printer.writeln()

    return printer.getvalue()