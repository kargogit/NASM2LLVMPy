import llvmlite.ir as ir
from typing import Dict, List, Optional

class FlagManager:
    def __init__(self):
        self.current_block: Optional[ir.Block] = None
        self.current_flags: Dict[str, ir.Value] = {}
        self.exit_flags: Dict[ir.Block, Dict[str, ir.Value]] = {}

    def fork(self) -> 'FlagManager':
        return FlagManager()

    def initialize_block(self, block: ir.Block, predecessors: List[ir.Block], builder: ir.IRBuilder):
        self.current_block = block
        self.current_flags = {}
        # Only initialize flags if explicitly needed (e.g., for SETcc instructions)
        if not predecessors:
            for flag in ['ZF']:  # Reduced to flags still in use
                self.current_flags[flag] = ir.Constant(ir.IntType(1), 0)

    def compute_flag(self, flag_name: str, builder: ir.IRBuilder, reg_manager) -> ir.Value:
        return self.current_flags.get(flag_name, ir.Constant(ir.IntType(1), 0))

    def finalize_block(self):
        if self.current_block is not None:
            self.exit_flags[self.current_block] = self.current_flags.copy()
