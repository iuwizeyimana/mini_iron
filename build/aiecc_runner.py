from __future__ import annotations

import subprocess
from pathlib import Path


def build_aiecc_command(
    mlir_path: str,
    kernel_object_files: list[str],
    out_dir: str = "build",
    xclbin_name: str = "final.xclbin",
    insts_name: str = "insts.bin",
    aiecc_exe: str = "aiecc.py",
    extra_args: list[str] | None = None,
) -> list[str]:
    """
    Build the aiecc.py command.
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    cmd = [
        aiecc_exe,
        "--aie-generate-xclbin",
        f"--xclbin-name={xclbin_name}",
        "--aie-generate-npu-insts",
        f"--npu-insts-name={insts_name}",
        mlir_path,
    ]

    cmd.extend(kernel_object_files)

    if extra_args:
        cmd.extend(extra_args)

    return cmd


def run_aiecc_command(
    cmd: list[str],
    cwd: str | None = None,
    dry_run: bool = False,
) -> None:
    """
    Execute the aiecc.py command.
    """
    if dry_run:
        print(" ".join(cmd))
        return

    subprocess.run(cmd, check=True, cwd=cwd)


def package_xclbin(
    mlir_path: str,
    kernel_object_files: list[str],
    out_dir: str = "build",
    xclbin_name: str = "final.xclbin",
    insts_name: str = "insts.bin",
    aiecc_exe: str = "aiecc.py",
    extra_args: list[str] | None = None,
    dry_run: bool = False,
) -> list[str]:
    """
    Build and optionally run the aiecc command.
    Returns the command for visibility/debugging.
    """
    cmd = build_aiecc_command(
        mlir_path=mlir_path,
        kernel_object_files=kernel_object_files,
        out_dir=out_dir,
        xclbin_name=xclbin_name,
        insts_name=insts_name,
        aiecc_exe=aiecc_exe,
        extra_args=extra_args,
    )
    run_aiecc_command(cmd, cwd=out_dir, dry_run=dry_run)
    return cmd