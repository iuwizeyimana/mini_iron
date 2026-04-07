# Simple command line entry point
import argparse
import importlib.util
from pathlib import Path

from validate.names import validate_unique_names
from validate.topology import validate_topology
from validate.placement import validate_placement
from validate.runtime import validate_runtime


from emit.emit_aie import emit_aie_module


def _load_program_from_python_file(py_file: str):
    path = Path(py_file)
    if not path.exists():
        raise FileNotFoundError(f"Input file does not exist: {py_file}")

    spec = importlib.util.spec_from_file_location("mini_iron_user_module", py_file)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load Python module from: {py_file}")

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not hasattr(mod, "program"):
        raise AttributeError(
            f"Expected top-level variable 'program' in {py_file}"
        )

    return mod.program


def main() -> None:
    parser = argparse.ArgumentParser(description="mini_iron CLI")
    parser.add_argument("input", help="Python design file that defines `program`")
    parser.add_argument(
        "--emit-mlir",
        action="store_true",
        help="Emit MLIR to stdout or --output",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validators",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output MLIR file path",
    )

    args = parser.parse_args()

    program = _load_program_from_python_file(args.input)

    if args.validate or args.emit_mlir:
        validate_unique_names(program)
        validate_topology(program)
        validate_placement(program)
        validate_runtime(program)

    if args.validate:
        print("Validation successful.")

    if args.emit_mlir:
        mlir_text = emit_aie_module(program)
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(mlir_text)
            print(f"Wrote MLIR to {out_path}")
        else:
            print(mlir_text)


if __name__ == "__main__":
    main()
