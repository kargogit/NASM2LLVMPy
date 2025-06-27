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
        self.current_registers: Dict[str, ir.Value] = {}
        self.exit_registers: Dict[ir.Block, Dict[str, ir.Value]] = {}

    def fork(self) -> 'RegisterManager':
        return RegisterManager()


    def initialize_block(self, block: ir.Block, predecessors: List[ir.Block], builder: ir.IRBuilder):
        self.current_block = block
        self.current_registers = {}


        if not predecessors:

            func = block.parent


            arg_registers = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]

            for reg in self.register_info:
                if reg.startswith('XMM'):
                    self.current_registers[reg] = ir.Constant(ir.VectorType(ir.FloatType(), 4), [0.0, 0.0, 0.0, 0.0])
                else:
                    self.current_registers[reg] = ir.Constant(self.get_register_type(reg), 0)





            for i, param in enumerate(func.args):
                if i < len(arg_registers):
                    reg_name = arg_registers[i]

                    param_val = param
                    reg_type = self.get_register_type(reg_name)
                    if param_val.type != reg_type:
                        param_val = builder.zext(param_val, reg_type)
                    self.current_registers[reg_name] = param_val
            return


        for reg in self.register_info:
            pred_values = []
            unique_values = set()

            for pred in predecessors:
                if pred in self.exit_registers and reg in self.exit_registers[pred]:
                    pred_val = self.exit_registers[pred][reg]
                else:

                    pred_val = ir.Constant(self.get_register_type(reg), 0)
                pred_values.append(pred_val)
                unique_values.add(str(pred_val))

            if len(unique_values) > 1:
                phi = builder.phi(self.get_register_type(reg), name=f"{reg}_phi")
                for pred, val in zip(predecessors, pred_values):
                    phi.add_incoming(val, pred)
                self.current_registers[reg] = phi
            else:
                self.current_registers[reg] = pred_values[0] if pred_values else ir.Constant(self.get_register_type(reg), 0)

    def get_register_type(self, reg_name: str) -> ir.Type:
        size = self.register_info[reg_name]['size']
        if size == 128:
            return ir.VectorType(ir.FloatType(), 4)  # 4 x float32
        return ir.IntType(size)


    def get_register_ssa(self, reg_name: str, builder: ir.IRBuilder) -> ir.Value:
        return self.current_registers.get(reg_name, ir.Constant(self.get_register_type(reg_name), 0))

    def set_register_ssa(self, reg_name: str, value: ir.Value, builder: ir.IRBuilder):

        if self.register_info[reg_name]['size'] == 64:
            if isinstance(value.type, ir.PointerType):
                value = builder.ptrtoint(value, ir.IntType(64))
            elif isinstance(value.type, ir.IntType) and value.type.width < 64:
                value = builder.zext(value, ir.IntType(64))



        current_reg = reg_name
        current_value = value
        while True:
            self.current_registers[current_reg] = current_value
            parent = self.register_info[current_reg].get('parent')
            if not parent:
                break

            parent_size = self.register_info[parent]['size']
            parent_type = ir.IntType(parent_size)
            offset = self.register_info[current_reg].get('offset')
            size = self.register_info[current_reg]['size']
            parent_value = self.current_registers.get(parent, ir.Constant(parent_type, 0))
            if size == 32 and parent_size == 64:
                new_parent_value = builder.zext(current_value, parent_type)
            else:
                mask = ((1 << size) - 1) << offset
                mask_val = ir.Constant(parent_type, mask)
                masked_parent = builder.and_(parent_value, builder.not_(mask_val))
                extended = builder.zext(current_value, parent_type)
                shifted = builder.shl(extended, ir.Constant(parent_type, offset))
                new_parent_value = builder.or_(masked_parent, shifted)
            current_reg = parent
            current_value = new_parent_value

    def finalize_block(self):
        if self.current_block is not None:
            self.exit_registers[self.current_block] = self.current_registers.copy()
