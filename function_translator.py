from typing import Dict, List, Optional, Union
from dataclasses import dataclass

import llvmlite.ir as ir
from module_data import FunctionData, BlockData, InstructionData, OperandData
from register_manager import RegisterManager
from control_flow_handler import ControlFlowHandler
from flag_manager import FlagManager
from module_data import ModuleData


@dataclass
class FunctionContext:
    func: ir.Function
    builder: ir.IRBuilder
    reg_manager: RegisterManager
    cf_handler: ControlFlowHandler
    flag_manager: FlagManager
    stack_vars: Dict[int, ir.AllocaInstr]


class FunctionTranslator:
    def __init__(self, llvm_generator):
        self.llvm_generator = llvm_generator
        self.module = llvm_generator.get_module()
        self.reg_manager = RegisterManager()
        self.cf_handler = ControlFlowHandler(self.module)
        self.flag_manager = FlagManager()

    def infer_parameter_types(self, func_data: FunctionData, param_registers: List[str]) -> List[ir.Type]:
        types = []
        entry_block = func_data.blocks[0] if func_data.blocks else None
        if not entry_block:
            return [ir.IntType(64)] * len(param_registers)

        usage = {reg: {'pointer': False, 'integer': False, 'size': 64} for reg in param_registers}

        for instr in entry_block.non_terminator_instructions + [entry_block.terminator_instruction]:
            if instr is None:
                continue


            for op in instr.operands:
                if op.type == 'register':
                    reg_name = op.register
                    current_reg = reg_name
                    parent_reg = None


                    while True:
                        reg_info = RegisterManager.register_info.get(current_reg, {})
                        parent_reg = reg_info.get('parent')
                        if not parent_reg:
                            break
                        current_reg = parent_reg

                    if current_reg in param_registers:

                        reg_size = RegisterManager.register_info.get(reg_name, {}).get('size', 64)
                        if reg_size < usage[current_reg]['size']:
                            usage[current_reg]['size'] = reg_size

                        if any(o.type == 'memory' and o.base == reg_name for o in instr.operands):
                            usage[current_reg]['pointer'] = True
                    elif reg_name in param_registers:

                        reg_size = RegisterManager.register_info.get(reg_name, {}).get('size', 64)
                        if reg_size < usage[reg_name]['size']:
                            usage[reg_name]['size'] = reg_size
                        if any(o.type == 'memory' and o.base == reg_name for o in instr.operands):
                            usage[reg_name]['pointer'] = True


            if instr.opcode.upper() == 'CALL' and instr.operands:
                target_operand = instr.operands[0]
                if target_operand.type == 'name':
                    func_name = target_operand.name
                    func = self.llvm_generator.module.globals.get(func_name)
                    func_type = None
                    if isinstance(func, ir.Function):
                        func_type = func.type.pointee
                    else:
                        func_type = self.llvm_generator.known_externs.get(func_name)

                    if func_type:
                        arg_registers = ['RDI', 'RSI', 'RDX', 'RCX', 'R8', 'R9']
                        for i, arg_reg in enumerate(arg_registers[:len(func_type.args)]):
                            if arg_reg not in param_registers:
                                continue
                            param_idx = param_registers.index(arg_reg)
                            expected_type = func_type.args[i]
                            if isinstance(expected_type, ir.PointerType):
                                usage[arg_reg]['pointer'] = True
                            elif isinstance(expected_type, ir.IntType):
                                usage[arg_reg]['size'] = expected_type.width



        for reg in param_registers:
            if usage[reg]['pointer']:
                types.append(ir.PointerType(ir.IntType(8)))
            elif usage[reg]['size'] == 32:
                types.append(ir.IntType(32))
            else:
                types.append(ir.IntType(64))


        if func_data.name == 'main' and len(types) > 1:
            types[1] = ir.PointerType(ir.PointerType(ir.IntType(8)))

        return types

    def declare_all_functions(self, module_data: ModuleData):
        for func_name, function in module_data.functions.items():
            if func_name == "_start":
                ir.Function(self.module, ir.FunctionType(ir.VoidType(), []), name=func_name)
            else:
                param_registers = function.parameter_regs
                param_types = self.infer_parameter_types(function, param_registers)
                func_type = ir.FunctionType(ir.IntType(64), param_types)
                ir.Function(self.module, func_type, name=func_name)

    def translate_all_functions(self, module_data):
        self.module_data = module_data
        for func_name, func_data in module_data.functions.items():
            self.translate_function_asm_to_llvm(func_data, func_name)

    def translate_PUSH(self, instr: InstructionData, context: FunctionContext):
        operand = instr.operands[0]
        if operand.type == "register":
            if operand.register == "RBP":
                pass
            else:
                val = context.reg_manager.get_register_ssa(operand.register, context.builder)
                rsp = context.reg_manager.get_register_ssa("RSP", context.builder)
                new_rsp = context.builder.sub(rsp, ir.Constant(ir.IntType(64), 8), name="new_rsp")
                ptr = context.builder.inttoptr(new_rsp, ir.PointerType(ir.IntType(64)), name="stack_ptr")
                context.builder.store(val, ptr)
                context.reg_manager.set_register_ssa("RSP", new_rsp, context.builder)
        else:
            raise NotImplementedError("PUSH with non-register operand not yet supported")


    def translate_POP(self, instr: InstructionData, context: FunctionContext):
        operand = instr.operands[0]
        if operand.type == "register":
            if operand.register == "RBP":
                pass
            else:
                rsp = context.reg_manager.get_register_ssa("RSP", context.builder)
                ptr = context.builder.inttoptr(rsp, ir.PointerType(ir.IntType(64)), name="stack_ptr")
                val = context.builder.load(ptr, name="pop_val")
                context.reg_manager.set_register_ssa(operand.register, val, context.builder)
                new_rsp = context.builder.add(rsp, ir.Constant(ir.IntType(64), 8), name="new_rsp")
                context.reg_manager.set_register_ssa("RSP", new_rsp, context.builder)
        else:
            raise NotImplementedError("POP to non-register operand not yet supported")

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


        dest_type = self.get_operand_type(dest, context)
        size = dest_type.width
        context.flag_manager.update_flags_after_and(result, size, context.builder)

    def analyze_stack_usage(self, func_data: FunctionData) -> Dict[int, ir.Type]:
        """Analyze RBP-based memory accesses to determine stack variable offsets."""
        displacements = set()
        for block in func_data.blocks:
            for instr in block.non_terminator_instructions + [block.terminator_instruction]:
                if instr is None:
                    continue
                for op in instr.operands:
                    if op.type == "memory" and op.base == "RBP" and op.displacement is not None:
                        displacements.add(op.displacement)

        return {disp: ir.IntType(64) for disp in displacements}


    def translate_function_asm_to_llvm(self, asm_func: FunctionData, func_name: str):
        func = self.create_llvm_function_prototype(func_name, asm_func)


        block_map = {}
        for block in asm_func.blocks:
            bb = func.append_basic_block(block.label)
            block_map[block.label] = bb

        entry_bb = block_map[asm_func.blocks[0].label]
        stack_layout = self.analyze_stack_usage(asm_func)
        builder = ir.IRBuilder(entry_bb)
        stack_vars = {disp: builder.alloca(var_type, name=f"local_{abs(disp)}") for disp, var_type in stack_layout.items()}
        context = FunctionContext(
            func=func,
            builder=builder,
            reg_manager=self.reg_manager.fork(),
            cf_handler=self.cf_handler.fork(),
            flag_manager=self.flag_manager.fork(),
            stack_vars=stack_vars
        )


        arg_registers = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]
        for i, (param, reg) in enumerate(zip(func.args, arg_registers[:len(func.args)])):
            param_val = param
            reg_type = context.reg_manager.get_register_type(reg)
            if param_val.type != reg_type:
                if isinstance(param_val.type, ir.PointerType) and isinstance(reg_type, ir.IntType):
                    param_val = builder.ptrtoint(param_val, reg_type)
                elif isinstance(param_val.type, ir.IntType) and isinstance(reg_type, ir.PointerType):
                    param_val = builder.inttoptr(param_val, reg_type)
                elif param_val.type.width < reg_type.width:
                    param_val = builder.zext(param_val, reg_type)
                elif param_val.type.width > reg_type.width:
                    param_val = builder.trunc(param_val, reg_type)
            context.reg_manager.set_register_ssa(reg, param_val, builder)


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
        return_type = ir.VoidType()

        for block in func_data.blocks:
            terminator = block.terminator_instruction
            if terminator and terminator.opcode.upper() == 'RET':
                current_type = ir.VoidType()

                for instr in block.non_terminator_instructions:
                    if instr.operands and instr.operands[0].type == 'register':
                        reg = instr.operands[0].register
                        if reg in ('RAX', 'EAX'):

                            if instr.opcode in ['MOV', 'ADD', 'SUB', 'XOR', 'AND', 'OR', 'LEA',
                                            'POP', 'INC', 'DEC', 'SHL', 'SHR', 'SAR', 'SAL',
                                            'SETNE', 'CDQE', 'MOVZX', 'MOVSX']:
                                size = 64 if reg == 'RAX' else 32
                                current_type = ir.IntType(size)
                                break

                if isinstance(current_type, ir.IntType):
                    if return_type == ir.VoidType() or current_type.width > return_type.width:
                        return_type = current_type


        if func_data.name in ["_start", "deregister_tm_clones", "frame_dummy", "__do_global_dtors_aux"]:
            return ir.VoidType()

        return return_type


    def create_llvm_function_prototype(self, func_name: str, func_data: FunctionData) -> ir.Function:

        if func_name.startswith("_ITM_"):
            return None

        if not func_name or func_name == "_":
            func_name = f"anon_func_{len(self.module.functions)}"

        existing_func = self.module.globals.get(func_name)
        if existing_func and isinstance(existing_func, ir.Function):
            return existing_func


        if func_name == "_start":
            return ir.Function(self.module, ir.FunctionType(ir.VoidType(), []), name=func_name)

        if func_name == "__libc_start_main":
            return self._create_libc_start_main_prototype()

        if func_name in ["deregister_tm_clones", "frame_dummy"]:
            func_type = ir.FunctionType(ir.VoidType(), [])
            return ir.Function(self.module, func_type, name=func_name)


        known_funcs = {
            'printf': ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True),
            'exit': ir.FunctionType(ir.VoidType(), [ir.IntType(32)]),
            'fopen': ir.FunctionType(ir.PointerType(ir.IntType(8)), [ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8))]),
            'fclose': ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))]),
            'feof': ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))]),
            'getc': ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))]),
            '__cxa_finalize': ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))]),
            '__ctype_b_loc': ir.FunctionType(ir.PointerType(ir.PointerType(ir.IntType(16))), []),
            '__gmon_start__': ir.FunctionType(ir.VoidType(), [])
        }
        if func_name in known_funcs:
            return ir.Function(self.module, known_funcs[func_name], name=func_name)

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

    def translate_MOV(self, instr: InstructionData, context: FunctionContext):
        dest, src = instr.operands
        src_val = self.resolve_operand(src, context)
        dest_type = self.get_operand_type(dest, context)


        if isinstance(src_val.type, ir.PointerType) and isinstance(dest_type, ir.IntType):
            src_val = context.builder.ptrtoint(src_val, dest_type)


        if src_val.type != dest_type:
            if isinstance(src_val.type, ir.IntType) and isinstance(dest_type, ir.IntType):
                if src_val.type.width > dest_type.width:
                    src_val = context.builder.trunc(src_val, dest_type)
                else:
                    src_val = context.builder.zext(src_val, dest_type)


        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, src_val, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(src_val, typed_ptr)


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


        zf = context.flag_manager.compute_flag('ZF', context.builder, context.reg_manager)


        cond = context.builder.icmp_unsigned('==', zf, ir.Constant(ir.IntType(1), 0))


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


        size = dest_val.type.width
        context.flag_manager.update_flags_after_shr(result, dest_val, shift_val, size, context.builder)

    def translate_ADD(self, instr: InstructionData, context: FunctionContext):
        dest = instr.operands[0]
        src = instr.operands[1]
        dest_type = self.get_operand_type(dest, context)
        lhs = self.resolve_operand(dest, context)
        rhs = self.resolve_operand(src, context, expected_type=dest_type)
        result = context.builder.add(lhs, rhs, name="add_result")
        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            dest_type = self.get_operand_type(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)
        size = lhs.type.width

        self.flag_manager.update_flags_after_add(result, lhs, rhs, size, context.builder)

    def translate_SUB(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("SUB instruction requires two operands")
        dest, src = instr.operands
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


        size = dest_type.width
        context.flag_manager.update_flags_after_sub(result, lhs, rhs, size, context.builder)


    def _get_call_args(self, func: Optional[ir.Function], context: FunctionContext) -> List[ir.Value]:
        if func and isinstance(func, ir.Function):
            param_types = func.type.pointee.args
            args = []
            arg_regs = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]


            for i, param_type in enumerate(param_types[:6]):
                reg = arg_regs[i]
                reg_val = context.reg_manager.get_register_ssa(reg, context.builder)

                if isinstance(param_type, ir.IntType):
                    if param_type.width < 64:
                        casted = context.builder.trunc(reg_val, param_type)
                    else:
                        casted = reg_val
                elif isinstance(param_type, ir.PointerType):
                    casted = context.builder.inttoptr(reg_val, param_type)
                else:
                    casted = reg_val
                args.append(casted)


            if len(param_types) > 6:
                rsp = context.reg_manager.get_register_ssa("RSP", context.builder)
                for i, param_type in enumerate(param_types[6:]):

                    offset = i * 8
                    stack_addr = context.builder.add(rsp, ir.Constant(ir.IntType(64), offset))
                    stack_ptr = context.builder.inttoptr(stack_addr, ir.PointerType(ir.IntType(64)))
                    stack_val = context.builder.load(stack_ptr, name=f"stack_arg_{i}")

                    if isinstance(param_type, ir.IntType):
                        if param_type.width < 64:
                            casted = context.builder.trunc(stack_val, param_type)
                        else:
                            casted = stack_val
                    elif isinstance(param_type, ir.PointerType):
                        casted = context.builder.inttoptr(stack_val, param_type)
                    else:
                        casted = stack_val
                    args.append(casted)

            return args
        else:

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


        result = context.builder.sub(lhs, rhs, name="cmp_result")


        size = lhs.type.width


        context.flag_manager.update_flags_after_sub(result, lhs, rhs, size, context.builder)

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

        size = dest_val.type.width
        context.flag_manager.update_flags_after_sar(result, dest_val, shift_val, size, context.builder)

    def translate_TEST(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("TEST instruction requires two operands")

        lhs = self.resolve_operand(instr.operands[0], context)
        rhs = self.resolve_operand(instr.operands[1], context)


        result = context.builder.and_(lhs, rhs, name="test_result")


        size = lhs.type.width


        context.flag_manager.update_flags_after_and(result, size, context.builder)


    def translate_XOR(self, instr: InstructionData, context: FunctionContext):
        if len(instr.operands) != 2:
            raise ValueError("XOR instruction requires two operands")

        dest, src = instr.operands
        src_val = self.resolve_operand(src, context)
        dest_val = self.resolve_operand(dest, context)


        result = context.builder.xor(dest_val, src_val, name="xor_result")


        if dest.type == "register":
            context.reg_manager.set_register_ssa(dest.register, result, context.builder)
        elif dest.type == "memory":
            ptr = self.calculate_memory_address(dest, context)
            dest_type = self.get_operand_type(dest, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(dest_type))
            context.builder.store(result, typed_ptr)
        else:
            raise NotImplementedError(f"XOR destination type {dest.type} not supported")


        dest_type = self.get_operand_type(dest, context)
        size = dest_type.width
        context.flag_manager.update_flags_after_xor(result, size, context.builder)

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

    def get_operand_type(self, operand: OperandData, context: FunctionContext) -> ir.Type:
        if operand.type == "register":
            return context.reg_manager.get_register_type(operand.register)
        elif operand.type == "memory":
            if operand.size == "byte":
                return ir.IntType(8)
            elif operand.size == "word":
                return ir.IntType(16)
            elif operand.size == "dword":
                return ir.IntType(32)
            elif operand.size == "qword" or operand.size is None:
                return ir.IntType(64)
            else:
                raise ValueError(f"Unknown memory size: {operand.size}")
        elif operand.type == "immediate":

            return ir.IntType(64)
        elif operand.type == "name":
            return ir.IntType(64)
        raise ValueError(f"Unknown operand type: {operand.type}")


    def resolve_operand(self, operand: OperandData, context: FunctionContext, expected_type: Optional[ir.Type] = None):
        if operand.type == "register":
            reg_name = operand.register
            reg_info = RegisterManager.register_info.get(reg_name, {})
            parent_reg = reg_info.get('parent')
            if parent_reg:

                parent_operand = OperandData(type='register', register=parent_reg)
                parent_val = self.resolve_operand(parent_operand, context)
                size = reg_info['size']
                offset = reg_info.get('offset', 0)


                if offset > 0:
                    shifted = context.builder.lshr(parent_val, ir.Constant(ir.IntType(64), offset))
                else:
                    shifted = parent_val


                truncated = context.builder.trunc(shifted, ir.IntType(size))

                return context.builder.zext(truncated, ir.IntType(64))
            else:
                return context.reg_manager.get_register_ssa(reg_name, context.builder)
        elif operand.type == "immediate":
            if expected_type and isinstance(expected_type, ir.IntType):
                return ir.Constant(expected_type, operand.immediate)
            else:
                return ir.Constant(ir.IntType(64), operand.immediate)
        elif operand.type == "memory":
            ptr = self.calculate_memory_address(operand, context)
            mem_type = self.get_operand_type(operand, context)
            typed_ptr = context.builder.bitcast(ptr, ir.PointerType(mem_type))
            return context.builder.load(typed_ptr)
        elif operand.type == "name":
            name = operand.name
            if operand.relocation == "..plt":
                func = self.module.get_global(name)
                if not func:
                    func_type = ir.FunctionType(ir.IntType(64), [ir.IntType(64)] * 6)
                    func = ir.Function(self.module, func_type, name=name)
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
                if global_var:
                    return context.builder.gep(
                        global_var,
                        [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)]
                    )
                else:
                    return ir.Constant(ir.IntType(64), 0)


    def calculate_memory_address(self, operand: OperandData, context: FunctionContext):

        if operand.type == "memory" and operand.base == "RBP" and operand.displacement in context.stack_vars:
            return context.stack_vars[operand.displacement]


        if operand.relocation == '..got' and operand.name:
            got_var = self.module.get_global(f".got.{operand.name}")
            if not got_var:
                got_var = ir.GlobalVariable(self.module, ir.IntType(64), name=f".got.{operand.name}")
                got_var.linkage = 'external'
                got_var.align = 8
            return got_var

        elif operand.is_rip_relative:

            if operand.name in self.module_data.label_to_section_offset:
                section_name, label_offset = self.module_data.label_to_section_offset[operand.name]
                if section_name in self.llvm_generator.section_globals:
                    section_global = self.llvm_generator.section_globals[section_name]
                    base_ptr = context.builder.bitcast(section_global, ir.PointerType(ir.IntType(8)))
                    total_offset = label_offset + (operand.displacement or 0)
                    offset_val = ir.Constant(ir.IntType(64), total_offset)
                    return context.builder.gep(base_ptr, [offset_val], inbounds=True)
            elif operand.name:

                global_var = self.module.get_global(operand.name)
                if global_var:

                    if isinstance(global_var, ir.Function):
                        return global_var

                    return context.builder.gep(global_var, [ir.Constant(ir.IntType(32), 0),
                                                        ir.Constant(ir.IntType(32), 0)])
                else:
                    return ir.Constant(ir.PointerType(ir.IntType(8)), None)


        if operand.type == "memory" and operand.name:
            if operand.name in self.module_data.label_to_section_offset:
                section_name, label_offset = self.module_data.label_to_section_offset[operand.name]
                if section_name in self.llvm_generator.section_globals:
                    section_global = self.llvm_generator.section_globals[section_name]
                    base_ptr = context.builder.bitcast(section_global, ir.PointerType(ir.IntType(8)))
                    total_offset = label_offset + (operand.displacement or 0)
                    offset_val = ir.Constant(ir.IntType(64), total_offset)
                    return context.builder.gep(base_ptr, [offset_val], inbounds=True)


        addr = ir.Constant(ir.IntType(64), 0)
        if operand.base:
            base_val = context.reg_manager.get_register_ssa(operand.base, context.builder)
            addr = context.builder.add(addr, base_val)
        if operand.index:
            index_val = context.reg_manager.get_register_ssa(operand.index, context.builder)
            scale = ir.Constant(ir.IntType(64), operand.scale or 1)
            scaled_index = context.builder.mul(index_val, scale)
            addr = context.builder.add(addr, scaled_index)
        if operand.displacement is not None:
            disp = ir.Constant(ir.IntType(64), operand.displacement)
            addr = context.builder.add(addr, disp)
        return context.builder.inttoptr(addr, ir.PointerType(ir.IntType(8)))
