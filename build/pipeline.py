from pathlib import Path

from ir.program import Program
from validate.names import validate_unique_names
from validate.topology import validate_topology
from validate.placement import validate_placement


from emit.emit_aie import emit_aie_module


def validate_program(program: Program) -> None:
    validate_unique_names(program)
    validate_topology(program)
    validate_placement(program)


def emit_mlir_file(program: Program, output_path: str) -> Path:
    validate_program(program)

    mlir_text = emit_aie_module(program)

    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(mlir_text)
    return out_path


def collect_kernel_sources(program: Program) -> list[str]:
    seen = set()
    ordered = []
    for kernel in program.kernels:
        if kernel.source_file not in seen:
            seen.add(kernel.source_file)
            ordered.append(kernel.source_file)
    return ordered


def plan_build_commands(
    program: Program,
    mlir_path: str,
    kernel_obj_dir: str = "build/kernels",
    xclbin_path: str = "build/final.xclbin",
    insts_path: str = "build/insts.bin",
) -> list[str]:
    """
    Return shell-command strings that a later build runner can execute.
    """
    kernel_sources = collect_kernel_sources(program)
    kernel_obj_dir_path = Path(kernel_obj_dir)

    commands: list[str] = []
    for src in kernel_sources:
        src_path = Path(src)
        obj_path = kernel_obj_dir_path / (src_path.stem + ".o")
        commands.append(
            f"clang++ -c {src_path} -o {obj_path}"
        )

    kernel_obj_args = " ".join(
        str(kernel_obj_dir_path / (Path(src).stem + ".o"))
        for src in kernel_sources
    )

    commands.append(
        f"aiecc.py --aie-generate-xclbin "
        f"--xclbin-name={Path(xclbin_path).name} "
        f"--aie-generate-npu-insts "
        f"--npu-insts-name={Path(insts_path).name} "
        f"{mlir_path} {kernel_obj_args}"
    )

    return commands


def build_plan_summary(program: Program, mlir_path: str) -> str:
    cmds = plan_build_commands(program, mlir_path=mlir_path)
    lines = ["Build plan:"]
    for i, cmd in enumerate(cmds, start=1):
        lines.append(f"  {i}. {cmd}")
    return "\n".join(lines)