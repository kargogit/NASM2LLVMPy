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


        if not predecessors:
            for flag in ['CF', 'ZF', 'SF', 'OF']:
                self.current_flags[flag] = ir.Constant(ir.IntType(1), 0)
            return

    def initialize_block(self, block: ir.Block, predecessors: List[ir.Block], builder: ir.IRBuilder):
        self.current_block = block
        self.current_flags = {}

        managed_flags = ['CF', 'ZF', 'SF', 'OF']


        if not predecessors:
            for flag in managed_flags:
                self.current_flags[flag] = ir.Constant(ir.IntType(1), 0)
            return

        for flag in managed_flags:
            pred_values = []

            for pred in predecessors:
                if pred in self.exit_flags and flag in self.exit_flags[pred]:
                    pred_val = self.exit_flags[pred][flag]
                else:

                    pred_val = ir.Constant(ir.IntType(1), 0)
                pred_values.append(pred_val)


            if len(pred_values) == 0 or len(set(str(v) for v in pred_values)) == 1:
                self.current_flags[flag] = pred_values[0] if pred_values else ir.Constant(ir.IntType(1), 0)
            else:
                phi = builder.phi(ir.IntType(1), name=f"{flag}_phi")
                for pred, val in zip(predecessors, pred_values):
                    phi.add_incoming(val, pred)
                self.current_flags[flag] = phi

    def update_flags_after_add(self, result: ir.Value, lhs: ir.Value, rhs: ir.Value, size: int, builder: ir.IRBuilder):
        int_type = ir.IntType(size)


        zf = builder.icmp_unsigned('==', result, ir.Constant(int_type, 0))


        sf = builder.icmp_signed('<', result, ir.Constant(int_type, 0))


        cf = builder.icmp_unsigned('<', result, lhs)


        lhs_sign = builder.icmp_signed('>=', lhs, ir.Constant(int_type, 0))
        rhs_sign = builder.icmp_signed('>=', rhs, ir.Constant(int_type, 0))
        result_sign = builder.icmp_signed('>=', result, ir.Constant(int_type, 0))
        same_sign = builder.icmp_unsigned('==', lhs_sign, rhs_sign)
        diff_sign = builder.icmp_unsigned('!=', lhs_sign, result_sign)
        of = builder.and_(same_sign, diff_sign)


        self.current_flags['ZF'] = zf
        self.current_flags['SF'] = sf
        self.current_flags['CF'] = cf
        self.current_flags['OF'] = of

    def update_flags_after_sub(self, result: ir.Value, lhs: ir.Value, rhs: ir.Value, size: int, builder: ir.IRBuilder):
        int_type = ir.IntType(size)


        zf = builder.icmp_unsigned('==', result, ir.Constant(int_type, 0))


        sf = builder.icmp_signed('<', result, ir.Constant(int_type, 0))


        cf = builder.icmp_unsigned('<', lhs, rhs)


        lhs_sign = builder.icmp_signed('>=', lhs, ir.Constant(int_type, 0))
        rhs_sign = builder.icmp_signed('>=', rhs, ir.Constant(int_type, 0))
        result_sign = builder.icmp_signed('>=', result, ir.Constant(int_type, 0))
        diff_sign = builder.icmp_unsigned('!=', lhs_sign, rhs_sign)
        result_diff = builder.icmp_unsigned('!=', lhs_sign, result_sign)
        of = builder.and_(diff_sign, result_diff)


        self.current_flags['ZF'] = zf
        self.current_flags['SF'] = sf
        self.current_flags['CF'] = cf
        self.current_flags['OF'] = of

    def update_flags_after_xor(self, result: ir.Value, size: int, builder: ir.IRBuilder):
        int_type = ir.IntType(size)


        zf = builder.icmp_unsigned('==', result, ir.Constant(int_type, 0))

        sf = builder.icmp_signed('<', result, ir.Constant(int_type, 0))

        cf = ir.Constant(ir.IntType(1), 0)
        of = ir.Constant(ir.IntType(1), 0)

        self.current_flags.update({'ZF': zf, 'SF': sf, 'CF': cf, 'OF': of})

    def update_flags_after_and(self, result: ir.Value, size: int, builder: ir.IRBuilder):
        """Update ZF, SF, CF, OF flags after AND operation."""
        int_type = ir.IntType(size)

        zf = builder.icmp_unsigned('==', result, ir.Constant(int_type, 0))

        sf = builder.icmp_signed('<', result, ir.Constant(int_type, 0))

        cf = ir.Constant(ir.IntType(1), 0)
        of = ir.Constant(ir.IntType(1), 0)

        self.current_flags.update({'ZF': zf, 'SF': sf, 'CF': cf, 'OF': of})

    def update_flags_after_sar(self, result: ir.Value, original: ir.Value, shift_val: ir.Value, size: int, builder: ir.IRBuilder):
        int_type = ir.IntType(size)
        zf = builder.icmp_unsigned('==', result, ir.Constant(int_type, 0))
        sf = builder.icmp_signed('<', result, ir.Constant(int_type, 0))


        cf = ir.Constant(ir.IntType(1), 0)
        if isinstance(shift_val, ir.Constant) and isinstance(shift_val.constant, int):
            shift_count = shift_val.constant
            if 0 < shift_count <= size:
                bit_pos = shift_count - 1
                mask = 1 << bit_pos
                masked = builder.and_(original, ir.Constant(int_type, mask))
                cf = builder.icmp_unsigned('!=', masked, ir.Constant(int_type, 0))


        of = ir.Constant(ir.IntType(1), 0)
        if isinstance(shift_val, ir.Constant) and shift_val.constant == 1:
            of = ir.Constant(ir.IntType(1), 0)

        self.current_flags.update({'ZF': zf, 'SF': sf, 'CF': cf, 'OF': of})

    def update_flags_after_shr(self, result: ir.Value, original: ir.Value, shift_val: ir.Value, size: int, builder: ir.IRBuilder):
        int_type = ir.IntType(size)


        zf = builder.icmp_unsigned('==', result, ir.Constant(int_type, 0))


        sf = builder.icmp_signed('<', result, ir.Constant(int_type, 0))


        cf = ir.Constant(ir.IntType(1), 0)
        if isinstance(shift_val, ir.Constant) and isinstance(shift_val.constant, int):
            shift_count = shift_val.constant
            if 0 < shift_count < size:
                bit_pos = shift_count - 1
                mask = 1 << bit_pos
                masked = builder.and_(original, ir.Constant(int_type, mask))
                cf = builder.icmp_unsigned('!=', masked, ir.Constant(int_type, 0))


        of = ir.Constant(ir.IntType(1), 0)
        if isinstance(shift_val, ir.Constant) and shift_val.constant == 1:
            original_msb = builder.icmp_signed('<', original, ir.Constant(int_type, 0))
            result_msb = builder.icmp_signed('<', result, ir.Constant(int_type, 0))
            of = builder.icmp_unsigned('!=', original_msb, result_msb)

        self.current_flags.update({'ZF': zf, 'SF': sf, 'CF': cf, 'OF': of})

    def update_flags_after_shl(self, result: ir.Value, original: ir.Value, shift_val: ir.Value, size: int, builder: ir.IRBuilder):
        int_type = ir.IntType(size)

        zf = builder.icmp_unsigned('==', result, ir.Constant(int_type, 0))

        sf = builder.icmp_signed('<', result, ir.Constant(int_type, 0))

        cf = ir.Constant(ir.IntType(1), 0)
        if isinstance(shift_val, ir.Constant) and isinstance(shift_val.constant, int):
            shift_count = shift_val.constant
            if 0 < shift_count <= size:
                bit_pos = size - shift_count
                mask = 1 << bit_pos
                masked = builder.and_(original, ir.Constant(int_type, mask))
                cf = builder.icmp_unsigned('!=', masked, ir.Constant(int_type, 0))

        of = ir.Constant(ir.IntType(1), 0)
        if isinstance(shift_val, ir.Constant) and shift_val.constant == 1:
            original_msb = builder.icmp_signed('<', original, ir.Constant(int_type, 0))
            result_msb = builder.icmp_signed('<', result, ir.Constant(int_type, 0))
            of = builder.icmp_unsigned('!=', original_msb, result_msb)

        self.current_flags.update({'ZF': zf, 'SF': sf, 'CF': cf, 'OF': of})

    def compute_flag(self, flag_name: str, builder: ir.IRBuilder, reg_manager) -> ir.Value:
        return self.current_flags.get(flag_name, ir.Constant(ir.IntType(1), 0))

    def finalize_block(self):
        if self.current_block is not None:
            self.exit_flags[self.current_block] = self.current_flags.copy()
