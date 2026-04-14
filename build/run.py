from __future__ import annotations

from pathlib import Path

from ir.program import Program
from emit.emit_aie import emit_aie_module
from validate.names import validate_unique_names
from validate.placement import validate_placement
from validate.topology import validate_topology
from validate.runtime import validate_runtime
from .kernel_compile import compile_kernels
from .aiecc_runner import package_xclbin


def validate_program(program: Program) -> None:
    """
    Run all currently available validators.
    """
    validate_unique_names(program)
    validate_topology(program)
    validate_placement(program)
    validate_runtime(program)


def write_mlir(program: Program, mlir_path: str) -> str:
    """
    Emit MLIR text and write it to disk.
    """
    mlir_text = emit_aie_module(program)
    out_path = Path(mlir_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(mlir_text)
    return str(out_path)


def build_program(
    program: Program,
    mlir_path: str = "build/aie.mlir",
    kernel_output_dir: str = "build/kernels",
    compiler: str = "clang++",
    compiler_flags: list[str] | None = None,
    out_dir: str = "build",
    xclbin_name: str = "final.xclbin",
    insts_name: str = "insts.bin",
    aiecc_exe: str = "aiecc.py",
    aiecc_extra_args: list[str] | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
   
    validate_program(program)

    mlir_file = write_mlir(program, mlir_path=mlir_path)

    kernel_object_files = compile_kernels(
        program=program,
        output_dir=kernel_output_dir,
        compiler=compiler,
        extra_flags=compiler_flags,
        dry_run=dry_run,
    )

    aiecc_cmd = package_xclbin(
        mlir_path=mlir_file,
        kernel_object_files=kernel_object_files,
        out_dir=out_dir,
        xclbin_name=xclbin_name,
        insts_name=insts_name,
        aiecc_exe=aiecc_exe,
        extra_args=aiecc_extra_args,
        dry_run=dry_run,
    )

    return {
        "mlir_path": mlir_file,
        "kernel_object_files": kernel_object_files,
        "aiecc_command": aiecc_cmd,
        "xclbin_path": str(Path(out_dir) / xclbin_name),
        "insts_path": str(Path(out_dir) / insts_name),
    }