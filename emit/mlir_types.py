from ir.types import DataType, TensorType


def emit_dtype(dtype: DataType) -> str:
    return dtype.name


def emit_memref_type(tensor_type: TensorType) -> str:
    dims = "x".join(str(d) for d in tensor_type.shape)
    return f"memref<{dims}x{emit_dtype(tensor_type.dtype)}>"