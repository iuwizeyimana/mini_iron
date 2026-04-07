from frontend.program_api import ProgramBuilder, fifo_endpoint, tensor
from validate.names import validate_unique_names
from validate.topology import validate_topology
from validate.placement import validate_placement

from emit.emit_aie import emit_aie_module

pb = ProgramBuilder(device_kind="npu1_1col")

shim = pb.tile("shim", 0, 0, kind="shim")
mem = pb.tile("mem", 0, 1, kind="mem")
core = pb.tile("core0", 0, 2, kind="core")

in_ty = tensor((64, 64), "i16")
out_ty = tensor((64, 64), "i32")

matmul = pb.kernel(
    name="matmul_i16_i32",
    source_file="kernels/matmul.cc",
    arg_types=[in_ty, in_ty, out_ty],
)

in_a = pb.object_fifo("inA", producer=shim, consumers=[core], depth=2, elem_type=in_ty)
in_b = pb.object_fifo("inB", producer=shim, consumers=[core], depth=2, elem_type=in_ty)
out_c = pb.object_fifo("outC", producer=core, consumers=[shim], depth=2, elem_type=out_ty)

worker = pb.worker("worker0", core)

in_a_ep = fifo_endpoint(in_a, "Consume")


worker.acquire(in_a_ep, alias="a")

worker.acquire(fifo_endpoint(in_b, "Consume"), alias="b")
worker.acquire(fifo_endpoint(out_c, "Produce"), alias="c")
worker.call(matmul, operands=["a", "b", "c"])
worker.release(fifo_endpoint(in_a, "Consume"))
worker.release(fifo_endpoint(in_b, "Consume"))
worker.release(fifo_endpoint(out_c, "Produce"))

program = pb.build()

validate_unique_names(program)
validate_topology(program)
validate_placement(program)

mlir_text = emit_aie_module(program)
print(mlir_text)