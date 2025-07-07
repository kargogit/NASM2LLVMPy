from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass

import llvmlite.ir as ir
from module_data import FunctionData, BlockData, InstructionData, OperandData
from register_manager import RegisterManager
from control_flow_handler import ControlFlowHandler
from flag_manager import FlagManager
from module_data import ModuleData
import logging
logging.basicConfig(level=logging.DEBUG)

@dataclass
class FunctionContext:
    func: ir.Function
    builder: ir.IRBuilder
    reg_manager: RegisterManager
    cf_handler: ControlFlowHandler
    flag_manager: FlagManager
    stack_vars: Dict[int, ir.AllocaInstr]
    saved_regs: Dict[str, ir.AllocaInstr]
    stack_frame: Optional[ir.AllocaInstr] = None
    current_offset: int = 0
    last_condition: Optional[Tuple[str, ir.Value, Optional[ir.Value]]] = None


class FunctionTranslator:
    def __init__(self, llvm_generator):
        self.llvm_generator = llvm_generator
        self.module = llvm_generator.get_module()
        self.reg_manager = RegisterManager()
        self.cf_handler = ControlFlowHandler(self.module)
        self.flag_manager = FlagManager()
        self.EXCLUDED_FUNCTIONS = {
            '_init', '_start', '_fini', 'deregister_tm_clones',
            '__do_global_dtors_aux', 'frame_dummy'
        }

    def infer_parameter_types(self, func_data: FunctionData, param_registers: List[str]) -> List[ir.Type]:
        types = []
        usage = {reg: {'pointer': False, 'size': 64} for reg in param_registers}

        for block in func_data.blocks:
            instructions = block.non_terminator_instructions + ([block.terminator_instruction] if block.terminator_instruction else [])
            for instr in instructions:
                if instr is None:
                    continue
                for op in instr.operands:
                    if op.type == 'register' and op.register in param_registers:
                        if any(o.type == 'memory' and (o.base == op.register or o.index == op.register) for o in instr.operands):
                            usage[op.register]['pointer'] = True
                        elif instr.opcode.upper() == 'CALL' and op == instr.operands[0]:
                            usage[op.register]['pointer'] = True
                        else:
                            reg_size = RegisterManager.register_info.get(op.register, {}).get('size', 64)
                            usage[op.register]['size'] = min(usage[op.register]['size'], reg_size)

        for reg in param_registers:
            if usage[reg]['pointer']:
                types.append(ir.PointerType(ir.IntType(8)))
            elif usage[reg]['size'] == 32:
                types.append(ir.IntType(32))
            else:
                types.append(ir.IntType(64))


        if func_data.name == 'main':
            types = [ir.IntType(32), ir.PointerType(ir.PointerType(ir.IntType(8)))] + types[2:]
        return types


    def declare_all_functions(self, module_data: ModuleData):
        for func_name, function in module_data.functions.items():
            if func_name in self.EXCLUDED_FUNCTIONS:
                continue
            if func_name == "_start":
                ir.Function(self.module, ir.FunctionType(ir.VoidType(), []), name=func_name)
            elif func_name == "main":
                param_types = self.infer_parameter_types(function, function.parameter_regs)
                func_type = ir.FunctionType(ir.IntType(32), param_types)
                ir.Function(self.module, func_type, name=func_name)
            else:
                param_registers = function.parameter_regs
                param_types = self.infer_parameter_types(function, param_registers)
                func_type = ir.FunctionType(ir.IntType(64), param_types)
                ir.Function(self.module, func_type, name=func_name)

    def translate_all_functions(self, module_data):
        self.module_data = module_data
        for func_name, func_data in module_data.functions.items():
            if func_name in self.EXCLUDED_FUNCTIONS:
                continue
            self.translate_function_asm_to_llvm(func_data, func_name)


    def translate_PUSH(self, instr: InstructionData, context: FunctionContext):
        operand = instr.operands[0]
        if operand.type == "register" and operand.register in context.saved_regs:
            val = context.reg_manager.get_register_ssa(operand.register, context.builder)
            context.builder.store(val, context.saved_regs[operand.register])

    def translate_POP(self, instr: InstructionData, context: FunctionContext):
        operand = instr.operands[0]
        if operand.type == "register" and operand.register in context.saved_regs:
            val = context.builder.load(context.saved_regs[operand.register], name=f"{operand.register}_restore")
            context.reg_manager.set_register_ssa(operand.register, val, context.builder)

    def translate_AND(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("AND instruction requires two operands")
        dest, src = instr.operands
        src_val = self.resolve_operand(src, context)
        dest_val = self.resolve_operand(dest, context)
        if src_val.type != dest_val.type:
            if src_val.type.width > dest_val.type.width:
                src_val = context.builder.trunc(src_val, dest_val.type)
            else:
                src_val = context.builder.zext(src_val, dest_val.type)
        result = context.builder.and_(dest_val, src_val, name="and_result")
        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            dest_type = self.get_operand_type(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)
        else:
            raise NotImplementedError(f"AND destination type {dest.type} not supported")
        context.last_condition = ("ARITH", result, None)

    def analyze_saved_registers(self, func_data: FunctionData) -> List[str]:
        saved_regs = []
        entry_block = func_data.blocks[0] if func_data.blocks else None
        if entry_block:
            for instr in entry_block.non_terminator_instructions:
                if instr.opcode.upper() == 'PUSH' and instr.operands[0].type == 'register':
                    reg = instr.operands[0].register
                    for block in func_data.blocks:
                        if block.terminator_instruction and block.terminator_instruction.opcode.upper() == 'RET':
                            for instr in block.non_terminator_instructions:
                                if (instr.opcode.upper() == 'POP' and
                                    instr.operands[0].type == 'register' and
                                    instr.operands[0].register == reg):
                                    saved_regs.append(reg)
                                    break
        return saved_regs


    def analyze_local_variables(self, func_data: FunctionData) -> Dict[int, Tuple[int, ir.Type]]:
        locals = {}
        for block in func_data.blocks:
            for instr in block.non_terminator_instructions + [block.terminator_instruction]:
                if instr is None:
                    continue
                for operand in instr.operands:
                    if operand.type == "memory" and operand.base == "RBP" and operand.displacement is not None:
                        offset = operand.displacement
                        size = {"byte": 8, "word": 16, "dword": 32, "qword": 64}.get(operand.size, 64)
                        ir_type = ir.IntType(size)
                        if offset in locals:
                            curr_size, curr_type = locals[offset]
                            if size > curr_size:
                                locals[offset] = (size, ir_type)
                        else:
                            locals[offset] = (size, ir_type)
        return locals


    def translate_function_asm_to_llvm(self, asm_func: FunctionData, func_name: str):
        func = self.create_llvm_function_prototype(func_name, asm_func)
        block_map = {block.label: func.append_basic_block(block.label) for block in asm_func.blocks}
        entry_bb = block_map[asm_func.blocks[0].label]
        builder = ir.IRBuilder(entry_bb)


        local_vars = self.analyze_local_variables(asm_func)
        context = FunctionContext(
            func=func,
            builder=builder,
            reg_manager=self.reg_manager.fork(),
            cf_handler=self.cf_handler.fork(),
            flag_manager=self.flag_manager.fork(),
            stack_vars={},
            saved_regs={}
        )
        for offset, (size, ir_type) in local_vars.items():
            alloca = builder.alloca(ir_type, name=f"local_{abs(offset)}")
            if size >= 128:
                alloca.align = 16
            elif size >= 64:
                alloca.align = 8
            else:
                alloca.align = 4
            context.stack_vars[offset] = alloca


        saved_regs = self.analyze_saved_registers(asm_func)
        for reg in saved_regs:
            reg_type = self.reg_manager.get_register_type(reg)
            context.saved_regs[reg] = builder.alloca(reg_type, name=f"saved_{reg.lower()}")

        arg_registers = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]
        seen_params = set()
        for i, (param, reg) in enumerate(zip(func.args, arg_registers[:len(func.args)])):
            if param in seen_params:
                continue
            param_val = param
            reg_type = context.reg_manager.get_register_type(reg)
            if param_val.type != reg_type:
                if isinstance(param_val.type, ir.PointerType) and isinstance(reg_type, ir.IntType):
                    param_val = builder.ptrtoint(param_val, reg_type)
                elif param_val.type.width < reg_type.width:
                    param_val = builder.zext(param_val, reg_type)
                elif param_val.type.width > reg_type.width:
                    param_val = builder.trunc(param_val, reg_type)
            context.reg_manager.set_register_ssa(reg, param_val, builder)
            seen_params.add(param)

        successors = {}

        conditional_jumps = {'JE', 'JNE', 'JG', 'JL', 'JA', 'JB', 'JAE', 'JBE', 'JC', 'JNC', 'JO', 'JNO', 'JS', 'JNS', 'JP', 'JNP', 'JZ', 'JNZ', 'JGE', 'JLE', 'JNS', 'JPO', 'JPE', 'JCXZ', 'JECXZ'}
        blocks_list = list(asm_func.blocks)
        for i, block in enumerate(blocks_list):
            terminator = block.terminator_instruction
            successors[block.label] = []


            if terminator is None:
                if i + 1 < len(blocks_list):
                    successors[block.label].append(blocks_list[i + 1].label)
                continue

            if terminator.opcode.upper() == 'JMP':
                if terminator.operands and terminator.operands[0].type == 'name':
                    target_label = terminator.operands[0].name
                    if target_label in block_map:
                        successors[block.label].append(target_label)
            elif terminator.opcode.upper() in conditional_jumps:
                if terminator.operands and terminator.operands[0].type == 'name':
                    target_label = terminator.operands[0].name
                    successors[block.label].append(target_label)
                    if i + 1 < len(blocks_list):
                        successors[block.label].append(blocks_list[i + 1].label)
            elif terminator.opcode.upper() == 'RET':
                successors[block.label] = []
            else:
                if i + 1 < len(blocks_list):
                    successors[block.label].append(blocks_list[i + 1].label)


        predecessors = {label: [] for label in block_map}
        for label, succ_labels in successors.items():
            for succ in succ_labels:
                if succ in predecessors:
                    predecessors[succ].append(label)


        for block in asm_func.blocks:
            pred_blocks = [block_map[pred_label] for pred_label in predecessors[block.label] if pred_label in block_map]
            self.translate_block_instructions(block, context, block_map[block.label], pred_blocks, successors)

        return func


    def _analyze_return_behavior(self, func_data: FunctionData) -> ir.Type:
        if self._function_sets_rax_before_ret(func_data):

            for block in func_data.blocks:
                if block.terminator_instruction and block.terminator_instruction.opcode.upper() == 'RET':
                    for instr in block.non_terminator_instructions:
                        if (instr.opcode.upper() == 'MOV' and
                            instr.operands[0].type == 'register' and
                            instr.operands[0].register == 'RAX'):
                            src = instr.operands[1]
                            if (src.type == 'name' or
                                (src.type == 'memory' and src.is_rip_relative) or
                                (instr.opcode.upper() == 'CALL' and
                                src.name in self.llvm_generator.known_externs and
                                isinstance(self.llvm_generator.known_externs[src.name].return_type, ir.PointerType))):
                                return ir.PointerType(ir.IntType(8))
            return ir.IntType(64)
        return ir.VoidType()


    def create_llvm_function_prototype(self, func_name: str, func_data: FunctionData) -> ir.Function:
        if func_name.startswith("_ITM_"):
            return None
        if not func_name or func_name == "_":
            func_name = f"anon_func_{len(self.module.functions)}"
        existing_func = self.module.globals.get(func_name)
        if existing_func and isinstance(existing_func, ir.Function):
            return existing_func


        if func_name == "main":
            param_types = [
                ir.IntType(32),
                ir.PointerType(ir.PointerType(ir.IntType(8))),
                ir.PointerType(ir.PointerType(ir.IntType(8)))
            ]
            func_type = ir.FunctionType(ir.IntType(32), param_types)
        elif func_name == "_start":
            func_type = ir.FunctionType(ir.VoidType(), [])
        elif func_name in self.llvm_generator.known_externs:
            func_type = self.llvm_generator.known_externs[func_name]
        else:
            return_type = self._analyze_return_behavior(func_data)
            param_registers = self._analyze_parameter_registers(func_data)
            param_types = [ir.IntType(64) for _ in param_registers]
            is_variadic = self._detect_variadic_function(func_data)
            func_type = ir.FunctionType(return_type, param_types, var_arg=is_variadic)

        func = ir.Function(self.module, func_type, name=func_name)
        self._set_function_attributes(func, func_name, is_variadic)
        return func


    def _create_libc_start_main_prototype(self) -> ir.Function:
        main_type = ir.FunctionType(
            ir.IntType(32),
            [ir.IntType(32), ir.PointerType(ir.PointerType(ir.IntType(8))),
            ir.PointerType(ir.PointerType(ir.IntType(8)))]
        )
        init_type = ir.FunctionType(ir.VoidType(), [])
        func_type = ir.FunctionType(
            ir.IntType(32),
            [
                ir.PointerType(main_type),
                ir.IntType(32),
                ir.PointerType(ir.PointerType(ir.IntType(8))),
                ir.PointerType(init_type),
                ir.PointerType(init_type),
                ir.PointerType(init_type),
                ir.PointerType(ir.IntType(8))
            ]
        )
        func = ir.Function(self.module, func_type, name="__libc_start_main")
        func.linkage = 'external'
        return func

    def _detect_variadic_function(self, func_data: FunctionData) -> bool:
        for block in func_data.blocks:
            for instr in block.non_terminator_instructions + [block.terminator_instruction]:
                if instr is None:
                    continue

                for op in instr.operands:
                    if op.type == "register" and op.register == "AL":
                        return True

                if instr.opcode.upper() in ["VA_START", "VA_ARG", "VA_END", "VA_COPY"]:
                    return True
        return False

    def _analyze_parameter_registers(self, func_data: FunctionData) -> List[str]:

        sysv_reg_order = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]


        param_registers = []
        written_regs = set()

        for block in func_data.blocks:
            for instr in block.non_terminator_instructions + [block.terminator_instruction]:
                if instr is None:
                    continue


                if instr.operands and instr.operands[0].type == "register":
                    written_regs.add(instr.operands[0].register)


                for op in instr.operands[1:]:
                    if op.type == "register" and op.register in sysv_reg_order:
                        if op.register not in written_regs and op.register not in param_registers:
                            param_registers.append(op.register)


        return [reg for reg in sysv_reg_order if reg in param_registers]

    def _set_function_attributes(self, func: ir.Function, func_name: str, is_variadic: bool):
        func.attributes.add('nounwind')
        if is_variadic:
            func.calling_convention = 'ccc'
        else:
            func.calling_convention = 'fastcc'
        if func_name.startswith('__libc_'):
            func.attributes.add('sspstrong')
        if func_name in self.llvm_generator.global_vars:
            func.linkage = 'external'
        if func_name.startswith("_ITM_"):
            pass

    def translate_block_instructions(self, block: BlockData, context: FunctionContext, bb: ir.Block, predecessors: List[ir.Block], successors):
        context.builder = ir.IRBuilder(bb)
        context.reg_manager.initialize_block(bb, predecessors, context.builder)
        for instr in block.non_terminator_instructions:
            self.handle_instruction(instr, context)
        succ_labels = successors[block.label]
        context.cf_handler.handle_terminator(block.terminator_instruction, context, succ_labels)

        context.reg_manager.finalize_block()

    def handle_instruction(self, instr: InstructionData, context: FunctionContext):
        opcode = instr.opcode.upper()
        handler = getattr(self, f"translate_{opcode}", self.unsupported_instruction)
        handler(instr, context)

    def unsupported_instruction(self, instr: InstructionData, context: FunctionContext):
        raise NotImplementedError(f"Unsupported instruction: {instr.opcode}")

    def _function_sets_rax_before_ret(self, func_data: FunctionData) -> bool:
        """Check if the function sets RAX (or subregisters) before any RET instruction."""
        return_regs = {'RAX', 'EAX', 'AX', 'AL'}
        for block in func_data.blocks:
            if block.terminator_instruction and block.terminator_instruction.opcode.upper() == 'RET':

                for instr in block.non_terminator_instructions:
                    if (instr.opcode.upper() in {'MOV', 'LEA', 'ADD', 'SUB', 'XOR', 'CALL'} and
                        instr.operands and instr.operands[0].type == 'register' and
                        instr.operands[0].register in return_regs):
                        return True

                if (block.non_terminator_instructions and
                    block.non_terminator_instructions[-1].opcode.upper() == 'CALL'):
                    target = block.non_terminator_instructions[-1].operands[0]
                    if target.type == 'name' and target.name in self.llvm_generator.known_externs:
                        return_type = self.llvm_generator.known_externs[target.name].return_type
                        return not isinstance(return_type, ir.VoidType)
        return False

    def translate_MOV(self, instr: InstructionData, context: FunctionContext):
        dest, src = instr.operands
        dest_type = self.get_operand_type(dest, context)
        src_val = self.resolve_operand(src, context, expected_type=dest_type)

        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, src_val, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(src_val, typed_ptr)


    def translate_XOR(self, instr: InstructionData, context: FunctionContext):
        dest, src = instr.operands
        dest_type = self.get_operand_type(dest, context)
        dest_val = self.resolve_operand(dest, context, expected_type=dest_type)
        src_val = self.resolve_operand(src, context, expected_type=dest_type)
        result = context.builder.xor(dest_val, src_val, name="xor_result")
        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)

        context.last_condition = ("ARITH", result, None)


    def translate_NOP(self, instr: InstructionData, context: FunctionContext):
        pass

    def translate_LEAVE(self, instr: InstructionData, context: 'FunctionContext'):
        rbp_current = context.reg_manager.get_register_ssa("RBP", context.builder)

        context.reg_manager.set_register_ssa("RSP", rbp_current, context.builder)

        pop_rbp_instr = InstructionData(
            opcode="POP",
            operands=[OperandData(type="register", register="RBP")]
        )
        self.translate_POP(pop_rbp_instr, context)

    def translate_SETNE(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 1:
            raise ValueError("SETNE instruction requires one operand")
        dest = instr.operands[0]
        if dest.type != "register":
            raise NotImplementedError("SETNE only supports register operands")
        if context.last_condition is None:
            raise ValueError("SETNE requires a preceding flag-setting instruction")

        cond_type, value1, value2 = context.last_condition
        if cond_type == "CMP":
            zf = context.builder.icmp_signed('==', value1, value2, name="zf")
        elif cond_type == "TEST":
            and_result = context.builder.and_(value1, value2, name="test_result")
            zf = context.builder.icmp_signed('==', and_result, ir.Constant(and_result.type, 0), name="zf")
        elif cond_type == "ARITH":
            zf = context.builder.icmp_signed('==', value1, ir.Constant(value1.type, 0), name="zf")
        else:
            raise ValueError(f"Unsupported condition type {cond_type} for SETNE")
        context.flag_manager.current_flags['ZF'] = zf
        cond = context.builder.icmp_unsigned('==', zf, ir.Constant(ir.IntType(1), 0), name="setne_cond")
        result = context.builder.select(cond, ir.Constant(ir.IntType(8), 1), ir.Constant(ir.IntType(8), 0))
        context.reg_manager.set_register_ssa(dest.register, result, context.builder)

    def translate_CDQE(self, instr: InstructionData, context: FunctionContext):

        eax_val = context.reg_manager.get_register_ssa("EAX", context.builder)

        rax_type = ir.IntType(64)

        sext_val = context.builder.sext(eax_val, rax_type, name="cdqe_sext")

        context.reg_manager.set_register_ssa("RAX", sext_val, context.builder)

    def translate_SHR(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("SHR instruction requires two operands")
        dest, src = instr.operands
        dest_val = self.resolve_operand(dest, context)
        shift_val = self.resolve_operand(src, context)
        if dest_val.type != shift_val.type:
            shift_val = context.builder.zext(shift_val, dest_val.type) if isinstance(shift_val.type, ir.IntType) else shift_val
        result = context.builder.lshr(dest_val, shift_val, name="shr_result")
        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            dest_type = self.get_operand_type(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)
        else:
            raise NotImplementedError(f"SHR destination type {dest.type} not supported")

        context.last_condition = ("ARITH", result, None)

    def translate_SHL(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("SHL instruction requires two operands")
        dest, src = instr.operands
        dest_val = self.resolve_operand(dest, context)
        shift_val = self.resolve_operand(src, context)
        if dest_val.type != shift_val.type:
            shift_val = context.builder.zext(shift_val, dest_val.type) if isinstance(shift_val.type, ir.IntType) else shift_val
        result = context.builder.shl(dest_val, shift_val, name="shl_result")
        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            dest_type = self.get_operand_type(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)
        else:
            raise NotImplementedError(f"SHL destination type {dest.type} not supported")

        context.last_condition = ("ARITH", result, None)

    def translate_ADD(self, instr: InstructionData, context: FunctionContext):
        dest = instr.operands[0]
        src = instr.operands[1]
        if dest.type == "register" and dest.register == "RSP" and src.type == "immediate":
            return
        dest_type = self.get_operand_type(dest, context)
        lhs = self.resolve_operand(dest, context)
        rhs = self.resolve_operand(src, context, expected_type=dest_type)
        result = context.builder.add(lhs, rhs, name="add_result")
        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)

        context.last_condition = ("ARITH", result, None)

    def translate_SUB(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("SUB instruction requires two operands")
        dest, src = instr.operands
        if dest.type == "register" and dest.register == "RSP" and src.type == "immediate":
            context.current_offset += src.immediate
            return
        dest_type = self.get_operand_type(dest, context)
        lhs = self.resolve_operand(dest, context)
        rhs = self.resolve_operand(src, context, expected_type=dest_type)
        if dest.type == "register" and lhs.type.width > dest_type.width:
            lhs = context.builder.trunc(lhs, dest_type)
        if src.type == "register" and rhs.type.width > dest_type.width:
            rhs = context.builder.trunc(rhs, dest_type)
        result = context.builder.sub(lhs, rhs, name="sub_result")
        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)

        context.last_condition = ("ARITH", result, None)


    def _get_call_args(self, func: Optional[ir.Function], context: FunctionContext) -> List[ir.Value]:
        if func and isinstance(func, ir.Function):
            param_types = func.type.pointee.args
            args = []
            arg_regs = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]
            for i, param_type in enumerate(param_types[:len(arg_regs)]):
                reg = arg_regs[i]
                reg_val = context.reg_manager.get_register_ssa(reg, context.builder)
                if isinstance(param_type, ir.PointerType) and isinstance(reg_val.type, ir.PointerType):
                    if reg_val.type != param_type:
                        reg_val = context.builder.bitcast(reg_val, param_type)
                elif isinstance(param_type, ir.IntType) and isinstance(reg_val.type, ir.PointerType):
                    reg_val = context.builder.ptrtoint(reg_val, param_type)
                elif isinstance(param_type, ir.IntType) and isinstance(reg_val.type, ir.IntType):
                    if reg_val.type.width < param_type.width:
                        reg_val = context.builder.zext(reg_val, param_type)
                    elif reg_val.type.width > param_type.width:
                        reg_val = context.builder.trunc(reg_val, param_type)
                args.append(reg_val)
            return args

        arg_regs = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]
        return [context.reg_manager.get_register_ssa(r, context.builder) for r in arg_regs]

    def translate_HLT(self, instr: InstructionData, context: FunctionContext):


        context.builder.unreachable()


    def translate_CMP(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("CMP instruction requires two operands")
        lhs = self.resolve_operand(instr.operands[0], context)
        rhs = self.resolve_operand(instr.operands[1], context)

        if lhs.type != rhs.type:
            if isinstance(lhs.type, ir.IntType) and isinstance(rhs.type, ir.IntType):
                if lhs.type.width < rhs.type.width:
                    lhs = context.builder.zext(lhs, rhs.type)
                else:
                    rhs = context.builder.zext(rhs, lhs.type)

        context.last_condition = ("CMP", lhs, rhs)

    def translate_MOVSX(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("MOVSX requires two operands")
        dest, src = instr.operands
        if dest.type != "register":
            raise NotImplementedError("MOVSX destination must be a register")


        dest_reg = dest.register
        dest_size = RegisterManager.register_info[dest_reg]['size']
        dest_type = ir.IntType(dest_size)


        if src.type == "register":
            src_reg = src.register
            src_size = RegisterManager.register_info[src_reg]['size']
            src_val = context.reg_manager.get_register_ssa(src_reg, context.builder)
        elif src.type == "memory":
            size_map = {"byte": 8, "word": 16, "dword": 32}
            if src.size not in size_map:
                raise ValueError(f"Unsupported memory size for MOVSX: {src.size}")
            src_size = size_map[src.size]
            ptr = self.calculate_memory_address(src, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(ir.IntType(src_size)))
            src_val = context.builder.load(typed_ptr)
        else:
            raise NotImplementedError("MOVSX source must be register or memory")


        if src_size >= dest_size:
            raise ValueError("MOVSX source size must be smaller than destination size")


        sext_val = context.builder.sext(src_val, dest_type, name=f"{dest_reg}_sext")
        context.reg_manager.set_register_ssa(dest_reg, sext_val, context.builder)

    def translate_MOVSXD(self, instr: InstructionData, context: FunctionContext):
        self.translate_MOVSX(instr, context)

    def translate_SAR(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("SAR instruction requires two operands")
        dest, src = instr.operands
        dest_val = self.resolve_operand(dest, context)
        shift_val = self.resolve_operand(src, context)
        if dest_val.type != shift_val.type:
            shift_val = context.builder.zext(shift_val, dest_val.type) if isinstance(shift_val.type, ir.IntType) else shift_val
        result = context.builder.ashr(dest_val, shift_val, name="sar_result")
        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            dest_type = self.get_operand_type(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)
        else:
            raise NotImplementedError(f"SAR destination type {dest.type} not supported")

        context.last_condition = ("ARITH", result, None)

    def translate_TEST(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("TEST instruction requires two operands")
        lhs = self.resolve_operand(instr.operands[0], context)
        rhs = self.resolve_operand(instr.operands[1], context)

        context.last_condition = ("TEST", lhs, rhs)

    def _get_function_type(self, name: str, module_data: ModuleData) -> ir.FunctionType:

        if name in self.llvm_generator.known_externs:
            return self.llvm_generator.known_externs[name]


        return ir.FunctionType(ir.IntType(64), [ir.IntType(64)]*6, var_arg=True)

    def translate_LEA(self, instr: InstructionData, context: FunctionContext):
        dest, src = instr.operands
        if src.type == "memory":

            ptr = self.calculate_memory_address(src, context)
            ptr_int = context.builder.ptrtoint(ptr, ir.IntType(64))
            context.reg_manager.set_register_ssa(dest.register, ptr_int, context.builder)
        elif src.type == "name" and src.relocation == "..plt":

            func_name = src.name
            func = self.module.get_global(func_name)
            if not func:

                func_type = self.llvm_generator.known_externs.get(func_name, ir.FunctionType(ir.VoidType(), []))
                func = ir.Function(self.module, func_type, name=func_name)

            ptr_int = context.builder.ptrtoint(func, ir.IntType(64))
            context.reg_manager.set_register_ssa(dest.register, ptr_int, context.builder)
        else:
            raise NotImplementedError(f"LEA with source type {src.type} not supported")

    def translate_MOVZX(self, instr: InstructionData, context: FunctionContext):
        dest, src = instr.operands
        if dest.type != "register":
            raise ValueError("MOVZX destination must be a register")


        dest_reg = dest.register
        dest_size = RegisterManager.register_info[dest_reg]['size']
        dest_type = ir.IntType(dest_size)


        src_val = self.resolve_operand(src, context)


        extended_val = context.builder.zext(src_val, dest_type, name=f"{dest_reg}_zext")

        context.reg_manager.set_register_ssa(dest_reg, extended_val, context.builder)

    def translate_MOVAPS(self, instr: InstructionData, context: FunctionContext):
        dest, src = instr.operands


        if src.type == "register" and src.register.startswith("XMM"):
            src_val = context.reg_manager.get_register_ssa(src.register, context.builder)
        else:
            raise NotImplementedError("MOVAPS source must be XMM register in this context")


        if dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)

            vec_ptr = context.builder.bitcast(ptr, ir.PointerType(ir.VectorType(ir.FloatType(), 4)))
            store_inst = context.builder.store(src_val, vec_ptr)
            store_inst.align = 16
        else:
            raise NotImplementedError("MOVAPS destination type not supported")

    def get_operand_type(self, operand: OperandData, context: FunctionContext) -> ir.Type:
        if operand.type == "register":
            return context.reg_manager.get_register_type(operand.register)
        elif operand.type == "memory":
            size_map = {
                "byte": ir.IntType(8),
                "word": ir.IntType(16),
                "dword": ir.IntType(32),
                "qword": ir.IntType(64),
                "oword": ir.VectorType(ir.FloatType(), 4)
            }
            return size_map.get(operand.size, ir.IntType(64))
        elif operand.type == "immediate":
            return ir.IntType(64)
        elif operand.type == "name":
            return ir.IntType(64)
        raise ValueError(f"Unknown operand type: {operand.type}")


    def resolve_operand(self, operand: OperandData, context: FunctionContext, expected_type: Optional[ir.Type] = None):
        if operand.type == "register":
            reg_name = operand.register
            value = context.reg_manager.get_register_ssa(reg_name, context.builder)
            reg_type = context.reg_manager.get_register_type(reg_name)
            if expected_type and value.type != expected_type:
                if isinstance(value.type, ir.PointerType) and isinstance(expected_type, ir.IntType):
                    value = context.builder.ptrtoint(value, expected_type)
                elif isinstance(value.type, ir.IntType) and isinstance(expected_type, ir.PointerType):
                    value = context.builder.inttoptr(value, expected_type)
                elif isinstance(value.type, ir.IntType) and isinstance(expected_type, ir.IntType):
                    if value.type.width < expected_type.width:
                        value = context.builder.zext(value, expected_type)
                    elif value.type.width > expected_type.width:
                        value = context.builder.trunc(value, expected_type)
                else:

                    if isinstance(value.type, ir.PointerType):
                        value = context.builder.ptrtoint(value, expected_type or reg_type)
            return value
        elif operand.type == "immediate":
            native_type = ir.IntType(32) if operand.immediate <= 0xFFFFFFFF else ir.IntType(64)
            value = ir.Constant(native_type, operand.immediate)
            if expected_type and expected_type != native_type:
                if native_type.width < expected_type.width:
                    return context.builder.zext(value, expected_type)
                elif native_type.width > expected_type.width:
                    return context.builder.trunc(value, expected_type)
            return value
        elif operand.type == "memory":
            ptr = self.calculate_memory_address(operand, context)
            mem_type = self.get_operand_type(operand, context)
            if expected_type and expected_type != mem_type:
                typed_ptr = context.builder.bitcast(ptr, ir.PointerType(expected_type))
                return context.builder.load(typed_ptr)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(mem_type))
            return context.builder.load(typed_ptr)
        elif operand.type == "name":
            value = self._resolve_name_operand(operand, context)
            if isinstance(value.type, ir.PointerType) and expected_type and not isinstance(expected_type, ir.PointerType):
                return context.builder.ptrtoint(value, expected_type)
            return value

    def _resolve_name_operand(self, operand: OperandData, context: FunctionContext):
        name = operand.name
        if name in self.llvm_generator.known_globals:
            return self.module.get_global(name)
        elif operand.relocation == "..plt":
            func = self.module.get_global(name) or ir.Function(self.module, ir.FunctionType(ir.IntType(64), [ir.IntType(64)] * 6), name=name)
            return func
        elif operand.relocation == "..got":
            got_var = self.module.get_global(f".got.{name}")
            if not got_var:
                got_var = ir.GlobalVariable(self.module, ir.IntType(64), name=f".got.{name}")
                got_var.linkage = 'external'
                got_var.align = 8
            return context.builder.load(got_var)
        else:
            global_var = self.module.get_global(name)
            return context.builder.gep(global_var, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)]) if global_var else ir.Constant(ir.IntType(64), 0)


    def get_type_size(self, ty: ir.Type) -> int:
        if isinstance(ty, ir.IntType):
            return ty.width // 8
        elif isinstance(ty, ir.PointerType):
            return 8
        else:
            raise NotImplementedError(f"Size calculation for type {ty} not implemented")

    def calculate_memory_address(self, operand: OperandData, context: FunctionContext):
        if operand.type != "memory":
            raise ValueError(f"Expected memory operand, got {operand.type}: {operand}")


        if operand.base in ["RBP", "RSP"] and operand.index is None:
            base_val = context.reg_manager.get_register_ssa(operand.base, context.builder)
            if operand.displacement in context.stack_vars:
                alloca = context.stack_vars[operand.displacement]
                return alloca
            else:
                offset = ir.Constant(ir.IntType(64), operand.displacement or 0)
                access_type = self.get_operand_type(operand, context)
                return context.builder.gep(base_val, [offset], inbounds=True)


        effective_address = None
        if operand.base:
            base_val = context.reg_manager.get_register_ssa(operand.base, context.builder)
            if isinstance(base_val.type, ir.PointerType):

                indices = []
                if operand.index:
                    index_val = context.reg_manager.get_register_ssa(operand.index, context.builder)
                    scale = ir.Constant(ir.IntType(64), operand.scale or 1)
                    scaled_index = context.builder.mul(index_val, scale)
                    indices.append(scaled_index)
                else:
                    indices.append(ir.Constant(ir.IntType(64), 0))
                if operand.displacement:
                    indices.append(ir.Constant(ir.IntType(64), operand.displacement))
                return context.builder.gep(base_val, indices, inbounds=True)
            effective_address = base_val

        if operand.index:
            if not effective_address:
                effective_address = ir.Constant(ir.IntType(64), 0)
            index_val = context.reg_manager.get_register_ssa(operand.index, context.builder)
            scale = ir.Constant(ir.IntType(64), operand.scale or 1)
            scaled_index = context.builder.mul(index_val, scale)
            effective_address = context.builder.add(effective_address, scaled_index)

        if operand.displacement is not None:
            if not effective_address:
                effective_address = ir.Constant(ir.IntType(64), 0)
            disp = ir.Constant(ir.IntType(64), operand.displacement)
            effective_address = context.builder.add(effective_address, disp)

        if effective_address:

            segment_base = (context.reg_manager.get_register_ssa(operand.segment, context.builder)
                        if operand.segment in ["FS", "GS"] else
                        ir.Constant(ir.IntType(64), 0))
            total_address = context.builder.add(segment_base, effective_address)
            access_type = self.get_operand_type(operand, context)
            return context.builder.inttoptr(total_address, ir.PointerType(access_type))


        if operand.is_rip_relative:
            if operand.name in self.module_data.label_to_section_offset:
                section_name, label_offset = self.module_data.label_to_section_offset[operand.name]
                if section_name in self.llvm_generator.section_globals:
                    section_global = self.llvm_generator.section_globals[section_name]
                    base_ptr = context.builder.bitcast(section_global, ir.PointerType(ir.IntType(8)))
                    byte_offset = label_offset + (operand.displacement or 0)
                    offset_val = ir.Constant(ir.IntType(64), byte_offset)
                    context.builder.add(ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0), name=f"nop_marker3-{offset_val}-{label_offset}-{byte_offset}-{operand.name}")
                    return context.builder.gep(base_ptr, [offset_val], inbounds=True)
            elif operand.name:
                global_var = self.module.get_global(operand.name)
                if global_var:
                    access_type = self.get_operand_type(operand, context)
                    if global_var.type.pointee != access_type:
                        return context.builder.bitcast(global_var, ir.PointerType(access_type))
                    return global_var
            raise ValueError(f"RIP-relative address for {operand.name} not resolvable")


        if operand.relocation == "..got" and operand.name:
            got_name = f".got.{operand.name}"
            got_var = self.module.get_global(got_name)
            if not got_var:
                access_type = self.get_operand_type(operand, context)
                got_var = ir.GlobalVariable(self.module, ir.IntType(64), name=got_name,
                                        linkage="external", alignment=8)
            return got_var

        raise ValueError(f"Unsupported memory operand: {operand}")
