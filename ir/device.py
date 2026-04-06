from dataclasses import dataclass

@dataclass
class DeviceModel:
    """
        Describes the target NPU device at a high level
        Not sure this is needed
        attributes: Kind, cols, row
        e.g: an NPU with 1x8 tiles kind: npu_1col; cols: 1, rows: 1
             Ryzen NPU with 4x8 kind: npu2, cols: 4, rows: 8
    """
    
    kind: str
    cols: str
    rows: int
    
    @staticmethod
    def from_kind(kind: str) -> "DeviceModel":
        # hardcoded table for start
        presets = {
            "npu1_1col": (1, 5), 
            "npu2": (4, 8),
        }
        
        if kind not in presets:
            raise ValueError(f"Unsupported device kind: {kind}")
        cols, rows = presets[kind]
        
        return DeviceModel(kind=kind, cols=cols, rows=rows)
    
    
    