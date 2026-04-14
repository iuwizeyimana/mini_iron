from __future__ import annotations

import subprocess
from pathlib import Path

from ir.program import Program


def collect_kernel_sources(program: Program) -> list[str]:
    """
    Return unique kernel source files in program order.
    """
    seen = set()
    ordered: list[str] = []
    for kernel in program.kernels:
        if kernel.source_file not in seen:
            seen.add(kernel.source_file)
            ordered.append(kernel.source_file)
    return ordered


def object_path_for_source(source_file: str, output_dir: str) -> Path:
    src = Path(source_file)
    return Path(output_dir) / f"{src.stem}.o"


def compile_command_for_source(
    source_file: str,
    output_dir: str,
    compiler: str = "clang++",
    extra_flags: list[str] | None = None,
) -> list[str]:
    """
    Build one compile command for a kernel source.
    """
    obj_path = object_path_for_source(source_file, output_dir)
    obj_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        compiler,
        "-c",
        source_file,
        "-o",
        str(obj_path),
    ]

    if extra_flags:
        cmd.extend(extra_flags)

    return cmd


def compile_commands_for_program(
    program: Program,
    output_dir: str = "build/kernels",
    compiler: str = "clang++",
    extra_flags: list[str] | None = None,
) -> list[list[str]]:
    """
    Generate all kernel compile commands for the program.
    """
    sources = collect_kernel_sources(program)
    return [
        compile_command_for_source(
            source_file=src,
            output_dir=output_dir,
            compiler=compiler,
            extra_flags=extra_flags,
        )
        for src in sources
    ]


def object_files_for_program(
    program: Program,
    output_dir: str = "build/kernels",
) -> list[str]:
    """
    Return the object files corresponding to the program's kernel sources.
    """
    return [
        str(object_path_for_source(src, output_dir))
        for src in collect_kernel_sources(program)
    ]


def run_compile_commands(
    commands: list[list[str]],
    dry_run: bool = False,
) -> None:
    """
    Execute compile commands sequentially.
    """
    for cmd in commands:
        if dry_run:
            print(" ".join(cmd))
            continue
        subprocess.run(cmd, check=True)


def compile_kernels(
    program: Program,
    output_dir: str = "build/kernels",
    compiler: str = "clang++",
    extra_flags: list[str] | None = None,
    dry_run: bool = False,
) -> list[str]:
    """
    Compile all kernel sources and return the object file paths.
    """
    commands = compile_commands_for_program(
        program=program,
        output_dir=output_dir,
        compiler=compiler,
        extra_flags=extra_flags,
    )
    run_compile_commands(commands, dry_run=dry_run)
    return object_files_for_program(program, output_dir=output_dir)