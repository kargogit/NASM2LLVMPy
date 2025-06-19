import llvmlite.ir as ir
from typing import List, Optional
from module_data import InstructionData, BlockData
from register_manager import RegisterManager

class ControlFlowHandler:
    CONDITION_MAP = {
        'JE':  ('ZF', True),
        'JZ':  ('ZF', True),
        'JNE': ('ZF', False),
        'JNZ': ('ZF', False),
        'JG':  ('SF_OF_ZF', (False, False)),
        'JGE': ('SF_OF', True),
        'JL':  ('SF_OF', False),
        'JLE': ('SF_OF_ZF', (True, True)),
        'JA':  ('CF_ZF', (False, False)),
        'JAE': ('CF', False),
        'JB':  ('CF', True),
        'JBE': ('CF_ZF', (True, True)),
        'JC':  ('CF', True),
        'JNC': ('CF', False),
        'JO':  ('OF', True),
        'JNO': ('OF', False),
        'JS':  ('SF', True),
        'JNS': ('SF', False),
        'JP':  ('PF', True),
        'JNP': ('PF', False),
        'JPE': ('PF', True),
        'JPO': ('PF', False),

    }

    def __init__(self, module: ir.Module):
        self.module = module

    def fork(self) -> 'ControlFlowHandler':
        return ControlFlowHandler(self.module)

    def handle_terminator(self, instr: Optional[InstructionData], context: 'FunctionContext', succ_labels: List[str]):
        if instr is None:
            self._handle_fallthrough(context, succ_labels)
        else:
            opcode = instr.opcode.upper()
            if opcode == 'CALL':
                self._handle_call(instr, context, succ_labels)
            elif opcode == 'JMP':
                self._handle_jmp(instr, context, succ_labels)
            elif opcode == 'RET':
                self._handle_ret(context)
            elif opcode in self.CONDITION_MAP:
                self._handle_conditional_jump(instr, context, succ_labels)
            else:
                self._handle_fallthrough(context, succ_labels)

    def _handle_fallthrough(self, context: 'FunctionContext', successors: List[str]):
        if not successors:
            context.builder.unreachable()
        else:
            next_block = self._get_block_by_label(context.func, successors[0])
            context.builder.branch(next_block)

    def _handle_call(self, instr: InstructionData, context: 'FunctionContext', succ_labels: List[str]):
        target = instr.operands[0]
        if target.type != "name":
            raise NotImplementedError("CALL with non-name target not supported yet")
        func_name = target.name

        func = self.module.get_global(func_name)
        if not func:

            called_function = module_data.functions.get(func_name)
            if called_function:
                param_types = [ir.IntType(64)] * len(called_function.parameter_regs)
                func_type = ir.FunctionType(ir.IntType(64), param_types)
                func = ir.Function(self.module, func_type, name=func_name)
        elif not isinstance(func, ir.Function):
            raise ValueError(f"Symbol '{func_name}' is not a function")

        arg_regs = ["RDI", "RSI", "RDX", "RCX", "R8", "R9"]
        args = []

        if func.function_type.var_arg:


            num_fixed_args = len(func.function_type.args)
            for i in range(num_fixed_args):
                reg = arg_regs[i]
                arg_val = context.reg_manager.get_register_ssa(reg, context.builder)
                expected_type = func.function_type.args[i]
                if isinstance(expected_type, ir.PointerType) and isinstance(arg_val.type, ir.IntType):
                    arg_val = context.builder.inttoptr(arg_val, expected_type)
                elif isinstance(expected_type, ir.IntType) and isinstance(arg_val.type, ir.IntType):
                    if expected_type.width < arg_val.type.width:
                        arg_val = context.builder.trunc(arg_val, expected_type)
                args.append(arg_val)

            for i in range(num_fixed_args, 6):
                reg = arg_regs[i]
                arg_val = context.reg_manager.get_register_ssa(reg, context.builder)
                args.append(arg_val)
        else:

            num_args = len(func.function_type.args)
            for i in range(min(6, num_args)):
                reg = arg_regs[i]
                arg_val = context.reg_manager.get_register_ssa(reg, context.builder)
                expected_type = func.function_type.args[i]
                if isinstance(expected_type, ir.IntType) and isinstance(arg_val.type, ir.IntType):
                    if expected_type.width < arg_val.type.width:
                        arg_val = context.builder.trunc(arg_val, expected_type)
                elif isinstance(expected_type, ir.PointerType) and isinstance(arg_val.type, ir.IntType):
                    arg_val = context.builder.inttoptr(arg_val, expected_type)
                args.append(arg_val)
            if num_args > 6:
                rsp = context.reg_manager.get_register_ssa("RSP", context.builder)
                for i in range(6, num_args):
                    offset = 8 * (i - 6)
                    stack_addr = context.builder.add(rsp, ir.Constant(ir.IntType(64), offset))
                    stack_ptr = context.builder.inttoptr(stack_addr, ir.PointerType(ir.IntType(64)))
                    arg_val = context.builder.load(stack_ptr, name=f"stack_arg_{i}")
                    expected_type = func.function_type.args[i]
                    if isinstance(expected_type, ir.PointerType) and isinstance(arg_val.type, ir.IntType):
                        arg_val = context.builder.inttoptr(arg_val, expected_type)
                    args.append(arg_val)
            if len(args) != len(func.function_type.args):
                raise ValueError(f"Argument mismatch: {func_name} expects {len(func.function_type.args)} args, got {len(args)}")

        call_result = context.builder.call(func, args, name=f"call_{func_name}")

        if not isinstance(func.function_type.return_type, ir.VoidType):
            context.reg_manager.set_register_ssa("RAX", call_result, context.builder)

        if not succ_labels or len(succ_labels) != 1:
            raise ValueError("CALL instruction must have exactly one successor")
        successor_bb = self._get_block_by_label(context.func, succ_labels[0])
        context.builder.branch(successor_bb)

    def _handle_jmp(self, instr: InstructionData, context: 'FunctionContext', succ_labels: List[str]):
        target = instr.operands[0]
        if target.type == 'name':

            func = self.module.globals.get(target.name)
            if func and isinstance(func, ir.Function):

                func_type = func.type.pointee
                if len(func_type.args) == 0:
                    if isinstance(func_type.return_type, ir.VoidType):

                        context.builder.call(func, [])
                        context.builder.unreachable()
                    else:

                        result = context.builder.call(func, [])
                        if func_type.return_type != context.func.type.pointee.return_type:

                            if func_type.return_type.width < context.func.type.pointee.return_type.width:
                                result = context.builder.zext(result, context.func.type.pointee.return_type)
                            else:
                                result = context.builder.trunc(result, context.func.type.pointee.return_type)
                        context.builder.ret(result)
                    return

        if succ_labels:
            target_bb = self._get_block_by_label(context.func, succ_labels[0])
            context.builder.branch(target_bb)
        else:
            context.builder.unreachable()

    def _handle_ret(self, context: 'FunctionContext'):
        func_return_type = context.func.type.pointee.return_type
        if isinstance(func_return_type, ir.VoidType):
            context.builder.ret_void()
        else:

            rax_val = context.reg_manager.get_register_ssa("RAX", context.builder)
            if rax_val.type != func_return_type:
                if isinstance(rax_val.type, ir.IntType) and isinstance(func_return_type, ir.IntType):
                    if rax_val.type.width > func_return_type.width:
                        rax_val = context.builder.trunc(rax_val, func_return_type)
                    else:
                        rax_val = context.builder.zext(rax_val, func_return_type)
            context.builder.ret(rax_val)

    def _handle_conditional_jump(self, instr: InstructionData, context: 'FunctionContext', succ_labels: List[str]):
        if len(succ_labels) < 2:
            context.builder.unreachable()
            return

        true_bb = self._get_block_by_label(context.func, succ_labels[0])
        false_bb = self._get_block_by_label(context.func, succ_labels[1])
        condition = self._resolve_condition(instr.opcode, context)
        context.builder.cbranch(condition, true_bb, false_bb)

    def _resolve_condition(self, opcode: str, context: 'FunctionContext') -> ir.Value:
        flag_type, flag_state = self.CONDITION_MAP[opcode.upper()]
        flags = flag_type.split('_')
        values = []

        for flag in flags:
            flag_val = context.flag_manager.compute_flag(flag, context.builder, context.reg_manager)
            values.append(flag_val)


        if len(flags) == 1:
            flag_val = values[0]
            if flag_state:
                return flag_val
            else:
                return context.builder.not_(flag_val)


        elif flag_type == 'SF_OF':
            sf, of = values
            if flag_state is True:
                return context.builder.icmp_signed('==', sf, of)
            else:
                return context.builder.icmp_signed('!=', sf, of)

        elif flag_type == 'CF_ZF':
            cf, zf = values
            if flag_state == (False, False):
                return context.builder.and_(
                    context.builder.not_(cf),
                    context.builder.not_(zf)
                )
            else:
                return context.builder.or_(cf, zf)

        elif flag_type == 'SF_OF_ZF':
            sf, of, zf = values
            if flag_state is False:
                sf_eq_of = context.builder.icmp_signed('==', sf, of)
                zf_zero = context.builder.icmp_unsigned('==', zf, ir.Constant(ir.IntType(1), 0))
                return context.builder.and_(sf_eq_of, zf_zero)
            else:
                sf_ne_of = context.builder.icmp_signed('!=', sf, of)
                return context.builder.or_(sf_ne_of, zf)

        else:
            raise NotImplementedError(f"Condition {flag_type} not implemented")

    def _get_block_by_label(self, func: ir.Function, label: str) -> ir.Block:
        for bb in func.basic_blocks:
            if bb.name == label:
                return bb
        raise ValueError(f"Block {label} not found in function {func.name}")

    def finalize_block_terminator(self, block: BlockData, builder: ir.IRBuilder, reg_manager: RegisterManager):
        if not builder.block.is_terminated:
            builder.unreachable()
