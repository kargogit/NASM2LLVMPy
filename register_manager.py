import llvmlite.ir as ir
from typing import Dict, List, Optional

class RegisterManager:


    register_info = {

        'XMM0': {'size': 128, 'parent': None, 'offset': 0},
        'XMM1': {'size': 128, 'parent': None, 'offset': 0},
        'XMM2': {'size': 128, 'parent': None, 'offset': 0},
        'XMM3': {'size': 128, 'parent': None, 'offset': 0},
        'XMM4': {'size': 128, 'parent': None, 'offset': 0},
        'XMM5': {'size': 128, 'parent': None, 'offset': 0},
        'XMM6': {'size': 128, 'parent': None, 'offset': 0},
        'XMM7': {'size': 128, 'parent': None, 'offset': 0},
        'XMM8': {'size': 128, 'parent': None, 'offset': 0},
        'XMM9': {'size': 128, 'parent': None, 'offset': 0},
        'XMM10': {'size': 128, 'parent': None, 'offset': 0},
        'XMM11': {'size': 128, 'parent': None, 'offset': 0},
        'XMM12': {'size': 128, 'parent': None, 'offset': 0},
        'XMM13': {'size': 128, 'parent': None, 'offset': 0},
        'XMM14': {'size': 128, 'parent': None, 'offset': 0},
        'XMM15': {'size': 128, 'parent': None, 'offset': 0},

        'RAX': {'size': 64, 'parent': None, 'offset': 0},
        'RBX': {'size': 64, 'parent': None, 'offset': 0},
        'RCX': {'size': 64, 'parent': None, 'offset': 0},
        'RDX': {'size': 64, 'parent': None, 'offset': 0},
        'RSI': {'size': 64, 'parent': None, 'offset': 0},
        'RDI': {'size': 64, 'parent': None, 'offset': 0},
        'RBP': {'size': 64, 'parent': None, 'offset': 0},
        'RSP': {'size': 64, 'parent': None, 'offset': 0},
        'R8': {'size': 64, 'parent': None, 'offset': 0},
        'R9': {'size': 64, 'parent': None, 'offset': 0},
        'R10': {'size': 64, 'parent': None, 'offset': 0},
        'R11': {'size': 64, 'parent': None, 'offset': 0},
        'R12': {'size': 64, 'parent': None, 'offset': 0},
        'R13': {'size': 64, 'parent': None, 'offset': 0},
        'R14': {'size': 64, 'parent': None, 'offset': 0},
        'R15': {'size': 64, 'parent': None, 'offset': 0},
        'FS': {'size': 64, 'parent': None, 'offset': 0},
        'GS': {'size': 64, 'parent': None, 'offset': 0},


        'EAX': {'size': 32, 'parent': 'RAX', 'offset': 0},
        'EBX': {'size': 32, 'parent': 'RBX', 'offset': 0},
        'ECX': {'size': 32, 'parent': 'RCX', 'offset': 0},
        'EDX': {'size': 32, 'parent': 'RDX', 'offset': 0},
        'ESI': {'size': 32, 'parent': 'RSI', 'offset': 0},
        'EDI': {'size': 32, 'parent': 'RDI', 'offset': 0},
        'EBP': {'size': 32, 'parent': 'RBP', 'offset': 0},
        'ESP': {'size': 32, 'parent': 'RSP', 'offset': 0},
        'R8D': {'size': 32, 'parent': 'R8', 'offset': 0},
        'R9D': {'size': 32, 'parent': 'R9', 'offset': 0},
        'R10D': {'size': 32, 'parent': 'R10', 'offset': 0},
        'R11D': {'size': 32, 'parent': 'R11', 'offset': 0},
        'R12D': {'size': 32, 'parent': 'R12', 'offset': 0},
        'R13D': {'size': 32, 'parent': 'R13', 'offset': 0},
        'R14D': {'size': 32, 'parent': 'R14', 'offset': 0},
        'R15D': {'size': 32, 'parent': 'R15', 'offset': 0},


        'AX': {'size': 16, 'parent': 'EAX', 'offset': 0},
        'BX': {'size': 16, 'parent': 'EBX', 'offset': 0},
        'CX': {'size': 16, 'parent': 'ECX', 'offset': 0},
        'DX': {'size': 16, 'parent': 'EDX', 'offset': 0},
        'SI': {'size': 16, 'parent': 'ESI', 'offset': 0},
        'DI': {'size': 16, 'parent': 'EDI', 'offset': 0},
        'BP': {'size': 16, 'parent': 'EBP', 'offset': 0},
        'SP': {'size': 16, 'parent': 'ESP', 'offset': 0},
        'R8W': {'size': 16, 'parent': 'R8D', 'offset': 0},
        'R9W': {'size': 16, 'parent': 'R9D', 'offset': 0},
        'R10W': {'size': 16, 'parent': 'R10D', 'offset': 0},
        'R11W': {'size': 16, 'parent': 'R11D', 'offset': 0},
        'R12W': {'size': 16, 'parent': 'R12D', 'offset': 0},
        'R13W': {'size': 16, 'parent': 'R13D', 'offset': 0},
        'R14W': {'size': 16, 'parent': 'R14D', 'offset': 0},
        'R15W': {'size': 16, 'parent': 'R15D', 'offset': 0},


        'AL': {'size': 8, 'parent': 'AX', 'offset': 0},
        'AH': {'size': 8, 'parent': 'AX', 'offset': 8},
        'BL': {'size': 8, 'parent': 'BX', 'offset': 0},
        'BH': {'size': 8, 'parent': 'BX', 'offset': 8},
        'CL': {'size': 8, 'parent': 'CX', 'offset': 0},
        'CH': {'size': 8, 'parent': 'CX', 'offset': 8},
        'DL': {'size': 8, 'parent': 'DX', 'offset': 0},
        'DH': {'size': 8, 'parent': 'DX', 'offset': 8},
        'SIL': {'size': 8, 'parent': 'SI', 'offset': 0},
        'DIL': {'size': 8, 'parent': 'DI', 'offset': 0},
        'BPL': {'size': 8, 'parent': 'BP', 'offset': 0},
        'SPL': {'size': 8, 'parent': 'SP', 'offset': 0},
        'R8B': {'size': 8, 'parent': 'R8W', 'offset': 0},
        'R9B': {'size': 8, 'parent': 'R9W', 'offset': 0},
        'R10B': {'size': 8, 'parent': 'R10W', 'offset': 0},
        'R11B': {'size': 8, 'parent': 'R11W', 'offset': 0},
        'R12B': {'size': 8, 'parent': 'R12W', 'offset': 0},
        'R13B': {'size': 8, 'parent': 'R13W', 'offset': 0},
        'R14B': {'size': 8, 'parent': 'R14W', 'offset': 0},
        'R15B': {'size': 8, 'parent': 'R15W', 'offset': 0},
    }

    def __init__(self):
        self.current_block: Optional[ir.Block] = None
        self.predecessors: List[ir.Block] = []
        self.current_registers: Dict[str, ir.Value] = {}
        self.exit_registers: Dict[ir.Block, Dict[str, ir.Value]] = {}
        self.defined_in_block: set = set()


    def fork(self) -> 'RegisterManager':
        return RegisterManager()


    def initialize_block(self, block: ir.Block, predecessors: List[ir.Block], builder: ir.IRBuilder):
        self.current_block = block
        self.predecessors = predecessors
        self.current_registers = {}
        self.defined_in_block = set()
        if not predecessors:

            for reg, reg_info in self.register_info.items():
                if not reg_info["parent"]:
                    if reg.startswith('XMM'):
                        self.current_registers[reg] = ir.Constant(ir.VectorType(ir.FloatType(), 4), [0.0, 0.0, 0.0, 0.0])
                    else:
                        self.current_registers[reg] = ir.Constant(self.get_register_type(reg), 0)
            func = block.parent
            arg_registers = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]
            for i, param in enumerate(func.args):
                if i < len(arg_registers):
                    reg_name = arg_registers[i]
                    param_val = param
                    reg_type = self.get_register_type(reg_name)
                    if param_val.type != reg_type:
                        if isinstance(param_val.type, ir.PointerType) and isinstance(reg_type, ir.IntType):
                            param_val = builder.ptrtoint(param_val, reg_type)
                        elif isinstance(param_val.type, ir.IntType) and isinstance(reg_type, ir.IntType):
                            if param_val.type.width < reg_type.width:
                                param_val = builder.zext(param_val, reg_type)
                            elif param_val.type.width > reg_type.width:
                                param_val = builder.trunc(param_val, reg_type)
                    self.current_registers[reg_name] = param_val
                    self.defined_in_block.add(reg_name)

    def get_register_type(self, reg_name: str) -> ir.Type:
        size = self.register_info[reg_name]['size']
        if size == 128:
            return ir.VectorType(ir.FloatType(), 4)
        return ir.IntType(size)


    def get_top_level_parent_and_offset(self, reg_name: str) -> tuple[str, int]:
        """Find the top-level parent register and total bit offset for a given register."""
        total_offset = 0
        current_reg = reg_name
        while True:
            info = self.register_info.get(current_reg)
            if not info or info['parent'] is None:
                return current_reg, total_offset
            total_offset += info['offset']
            current_reg = info['parent']


    def get_register_ssa(self, reg_name: str, builder: ir.IRBuilder) -> ir.Value:
        if reg_name in self.defined_in_block:
            return self.current_registers.get(reg_name, ir.Constant(self.get_register_type(reg_name), 0))

        top_reg, offset = self.get_top_level_parent_and_offset(reg_name)
        size = self.register_info[reg_name]['size']


        if top_reg == reg_name and self.predecessors:
            pred_values = []
            unique_values = set()
            for pred in self.predecessors:
                pred_val = (self.exit_registers.get(pred, {}).get(reg_name) or
                            ir.Constant(self.get_register_type(reg_name), 0))
                pred_values.append(pred_val)
                unique_values.add(str(pred_val))

            if len(unique_values) > 1:

                original_block = builder.block

                builder.position_at_start(self.current_block)

                phi = builder.phi(self.get_register_type(reg_name), name=f"{reg_name}_phi")
                for pred, val in zip(self.predecessors, pred_values):
                    phi.add_incoming(val, pred)

                builder.position_at_end(original_block)
                self.current_registers[reg_name] = phi
                return phi
            else:

                value = pred_values[0] if pred_values else ir.Constant(self.get_register_type(reg_name), 0)
                self.current_registers[reg_name] = value
                return value


        if top_reg in self.current_registers:
            top_val = self.current_registers[top_reg]
        elif self.predecessors:

            top_val = self.get_register_ssa(top_reg, builder)
        else:
            top_val = ir.Constant(self.get_register_type(top_reg), 0)


        if offset == 0 and size in [8, 16, 32, 64]:

            return builder.trunc(top_val, ir.IntType(size), name=f"{reg_name}_trunc")
        else:

            if offset != 0:
                shifted = builder.lshr(top_val, ir.Constant(top_val.type, offset), name=f"{reg_name}_shift")
            else:
                shifted = top_val
            mask = (1 << size) - 1
            masked = builder.and_(shifted, ir.Constant(shifted.type, mask), name=f"{reg_name}_mask")
            return builder.trunc(masked, ir.IntType(size), name=f"{reg_name}_val")


    def set_register_ssa(self, reg_name: str, value: ir.Value, builder: ir.IRBuilder):
        reg_type = self.get_register_type(reg_name)
        if isinstance(value.type, ir.PointerType) and reg_type.width == 64:
            value = builder.ptrtoint(value, reg_type)
        elif value.type != reg_type:
            if isinstance(value.type, ir.IntType):
                if value.type.width < reg_type.width:

                    value = builder.zext(value, reg_type)
                elif value.type.width > reg_type.width:
                    value = builder.trunc(value, reg_type)
            else:
                raise TypeError(f"Expected integer type for {reg_name}, got {value.type}")
        self.current_registers[reg_name] = value
        self.defined_in_block.add(reg_name)


        current_reg = reg_name
        current_value = value
        while True:
            parent = self.register_info[current_reg].get('parent')
            if not parent:
                break
            parent_type = self.get_register_type(parent)
            offset = self.register_info[current_reg].get('offset', 0)
            size = self.register_info[current_reg]['size']
            parent_value = self.current_registers.get(parent, ir.Constant(parent_type, 0))
            mask = (1 << size) - 1
            masked_parent = builder.and_(parent_value, ir.Constant(parent_type, ~(mask << offset)))

            shifted_value = builder.shl(builder.zext(current_value, parent_type), ir.Constant(parent_type, offset))
            new_parent_value = builder.or_(masked_parent, shifted_value)
            self.current_registers[parent] = new_parent_value
            self.defined_in_block.add(parent)
            current_reg = parent
            current_value = new_parent_value

    def finalize_block(self):
        if self.current_block is not None:
            self.exit_registers[self.current_block] = self.current_registers.copy()
