import llvmlite.ir as ir
from module_data import ModuleData, SectionData
from typing import Dict, List, Optional, Tuple, Union

class LLVMGenerator:
    def __init__(self, module_name: str, target_triple: str = "x86_64-pc-linux-gnu"):
        self.module = ir.Module(name=module_name)
        self.module.triple = target_triple
        self.module.data_layout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
        self.global_vars: Dict[str, ir.GlobalVariable] = {}
        self.string_literals: Dict[str, ir.GlobalVariable] = {}
        self.section_globals = {}
        self.known_globals = {
            'stdout': ir.PointerType(ir.IntType(8)),
            'stderr': ir.PointerType(ir.IntType(8)),
            'optind': ir.IntType(32),
        }
        self.known_externs = {

            '__libc_start_main': ir.FunctionType(
                ir.IntType(32),
                [
                    ir.PointerType(ir.FunctionType(
                        ir.IntType(32),
                        [ir.IntType(32),
                        ir.PointerType(ir.PointerType(ir.IntType(8))),
                        ir.PointerType(ir.PointerType(ir.IntType(8)))
                        ]
                    )),
                    ir.IntType(32),
                    ir.PointerType(ir.PointerType(ir.IntType(8))),
                    ir.PointerType(ir.FunctionType(ir.VoidType(), [])),
                    ir.PointerType(ir.FunctionType(ir.VoidType(), [])),
                    ir.PointerType(ir.FunctionType(ir.VoidType(), [])),
                    ir.PointerType(ir.IntType(8))
                ]
            ),

            'printf': ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True),
            'fopen': ir.FunctionType(ir.PointerType(ir.IntType(8)),
                                    [ir.PointerType(ir.IntType(8)),
                                    ir.PointerType(ir.IntType(8))]),
            'fclose': ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))]),
            'feof': ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))]),
            'getc': ir.FunctionType(ir.IntType(32), [ir.PointerType(ir.IntType(8))]),
            'exit': ir.FunctionType(ir.VoidType(), [ir.IntType(32)]),
            '__cxa_finalize': ir.FunctionType(ir.VoidType(), [ir.PointerType(ir.IntType(8))]),
            '__ctype_b_loc': ir.FunctionType(ir.PointerType(ir.PointerType(ir.IntType(16))), []),
            '__gmon_start__': ir.FunctionType(ir.VoidType(), []),
            '_ITM_deregisterTMCloneTable': ir.FunctionType(ir.VoidType(), []),
            '_ITM_registerTMCloneTable': ir.FunctionType(ir.VoidType(), [])
        }

    def generate(self, module_data: ModuleData):
        self.create_tm_clone_stubs()
        self.create_got_entries(module_data)
        self.create_global_variables(module_data)
        self.create_global_symbols(module_data)
        self.declare_externals(module_data)
        self.setup_global_ctors(module_data)
        self.setup_global_dtors(module_data)
        return self.module

    def create_tm_clone_stubs(self):

        void_func_type = ir.FunctionType(ir.VoidType(), [])


        deregister_func = ir.Function(self.module, void_func_type, name="_ITM_deregisterTMCloneTable")
        deregister_func.linkage = 'external'


        register_func = ir.Function(self.module, void_func_type, name="_ITM_registerTMCloneTable")
        register_func.linkage = 'external'

    def create_got_entries(self, module_data: ModuleData):
        for symbol in module_data.got_symbols:
            got_var = ir.GlobalVariable(self.module, ir.IntType(64), name=f".got.{symbol}")
            got_var.linkage = 'external'
            got_var.align = 8

    def create_global_variables(self, module_data: ModuleData):
        for section in module_data.sections:
            if section.name in [".rodata", ".data", ".bss", ".rodata.str"]:
                self._create_section_global(section)

    def create_global_symbols(self, module_data: ModuleData):
        for symbol in module_data.global_symbols:
            if symbol not in module_data.functions and symbol not in self.module.globals:
                global_var = ir.GlobalVariable(
                    self.module,
                    ir.ArrayType(ir.IntType(8), 1),
                    name=symbol
                )
                global_var.linkage = 'external'
                global_var.align = 1

    def _create_section_global(self, section: SectionData):
        if section.name == ".bss":
            self._create_bss_section(section)
        else:
            self._create_initialized_section(section)

    def _create_bss_section(self, section: SectionData):
        size = sum(size for size, _, _ in section.data)
        global_var = ir.GlobalVariable(
            self.module,
            ir.ArrayType(ir.IntType(8), size),
            name=section.name.lstrip('.')
        )
        global_var.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), size), [0] * size)
        global_var.linkage = 'common'
        global_var.align = section.alignment
        self.global_vars[section.name] = global_var
        self.section_globals[section.name] = global_var

    def _create_initialized_section(self, section: SectionData):
        data = []
        relocations = []
        current_offset = 0

        for size, value, dd_type in section.data:


            if dd_type == "integer":
                if value is None:
                    data.extend([0] * size)
                else:
                    data.extend(self._int_to_bytes(value, size))
                current_offset += size
            elif dd_type == "string":

                string_bytes = value.encode('utf-8')
                if not string_bytes.endswith(b'\x00'):
                    string_bytes += b'\x00'
                    size += 1
                if len(string_bytes) >= size:
                    data.extend(string_bytes[:size])
                else:
                    data.extend(string_bytes + [0] * (size - len(string_bytes)))
                current_offset += size
            elif dd_type == "name":

                relocations.append((current_offset, size, value))
                data.extend([0] * size)
                current_offset += size
            else:

                data.extend([0] * size)
                current_offset += size

        if section.alignment > 1:
            final_aligned_size = ((current_offset + section.alignment - 1) // section.alignment) * section.alignment
            data.extend([0] * (final_aligned_size - current_offset))


        global_var = ir.GlobalVariable(
            self.module,
            ir.ArrayType(ir.IntType(8), len(data)),
            name=section.name.lstrip('.')
        )
        global_var.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len(data)), data)
        global_var.linkage = 'private'
        global_var.align = section.alignment
        self.global_vars[section.name] = global_var
        self.section_globals[section.name] = global_var

        if relocations:
            self._add_relocation_metadata(global_var, relocations)


    def _int_to_bytes(self, value: int, size: int) -> List[int]:
        return [(value >> (i * 8)) & 0xFF for i in range(size)]

    def _get_or_create_string_literal(self, content: str) -> ir.GlobalVariable:
        if content in self.string_literals:
            return self.string_literals[content]


        str_bytes = content.encode('utf-8') + b'\x00'
        str_type = ir.ArrayType(ir.IntType(8), len(str_bytes))
        str_global = ir.GlobalVariable(
            self.module,
            str_type,
            name=f".str.{len(self.string_literals)}"
        )
        str_global.initializer = ir.Constant(str_type, bytearray(str_bytes))
        str_global.linkage = 'private'
        str_global.align = 1

        self.string_literals[content] = str_global
        return str_global

    def _add_relocation_metadata(self, global_var: ir.GlobalVariable, relocations: List[Tuple[int, int, str]]):
        if not relocations:
            return

        md_name = f"{global_var.name}.relocations"
        md_node = self.module.add_named_metadata(md_name)

        for offset, size, target in relocations:
            if target.startswith(".str."):
                target_var = self.module.get_global(target)
                if not target_var:
                    raise ValueError(f"String literal {target} not found")
                md_entry = [
                    ir.Constant(ir.IntType(64), offset),
                    ir.Constant(ir.IntType(32), size),
                    target_var
                ]
            else:
                md_entry = [
                    ir.Constant(ir.IntType(64), offset),
                    ir.Constant(ir.IntType(32), size),
                    ir.MetaDataString(self.module, target)
                ]
            md_node.add(md_entry)

    def declare_externals(self, module_data: ModuleData):
            for symbol in module_data.extern_symbols:
                if symbol in self.module.globals:
                    continue
                if symbol in self.known_globals:
                    global_var = ir.GlobalVariable(
                        self.module,
                        self.known_globals[symbol],
                        name=symbol
                    )
                    global_var.linkage = 'external'
                    global_var.align = 8
                else:
                    func_type = self.known_externs.get(
                        symbol,
                        ir.FunctionType(ir.IntType(64), [ir.IntType(64)], var_arg=True)
                    )
                    func = ir.Function(self.module, func_type, name=symbol)
                    func.linkage = 'external'

    def _get_priority_from_label(self, label: str) -> int:
        parts = label.split('.')
        for part in parts:
            if part.isdigit():
                return int(part)
        return 10

    def setup_global_ctors(self, module_data: ModuleData):
        init_array = next((s for s in module_data.sections if s.name == ".init_array"), None)
        if not init_array:
            return

        ctors = []
        current_offset = 0

        for size, value, dd_type in init_array.data:
            if isinstance(value, str):

                priority = 65535

                if current_offset in init_array.labels:

                    pass


                func_type = ir.FunctionType(ir.VoidType(), [])
                func = self.module.get_global(value)
                if not func:
                    func = ir.Function(self.module, func_type, name=value)
                ctors.append((priority, func))

            current_offset += size

        if not ctors:
            return


        ctor_struct = ir.LiteralStructType([
            ir.IntType(32),
            ir.PointerType(ir.FunctionType(ir.VoidType(), [])),
            ir.PointerType(ir.IntType(8))
        ])
        ctor_array = ir.ArrayType(ctor_struct, len(ctors))

        global_ctors = ir.GlobalVariable(
            self.module,
            ctor_array,
            name="llvm.global_ctors"
        )
        global_ctors.initializer = ir.Constant(ctor_array, [
            ir.Constant(ctor_struct, (ir.Constant(ir.IntType(32), prio), func, ir.Constant(ir.IntType(8).as_pointer(), None)))
            for prio, func in ctors
        ])
        global_ctors.linkage = 'appending'
        global_ctors.align = 8

    def setup_global_dtors(self, module_data: ModuleData):
        fini_array = next((s for s in module_data.sections if s.name == ".fini_array"), None)
        if not fini_array:
            return

        dtors = []
        current_offset = 0
        for size, value, ddtype in fini_array.data:
            if isinstance(value, str):
                priority = 65535
                if current_offset in fini_array.labels:
                    for label in fini_array.labels[current_offset]:
                        priority = self._get_priority_from_label(label)
                        break
                func_type = ir.FunctionType(ir.VoidType(), [])
                func = self.module.get_global(value)
                if not func:
                    func = ir.Function(self.module, func_type, name=value)
                dtors.append((priority, func))
            current_offset += size

        dtors.reverse()

        if not dtors:
            return

        dtor_struct = ir.LiteralStructType([
            ir.IntType(32),
            ir.PointerType(ir.FunctionType(ir.VoidType(), [])),
            ir.PointerType(ir.IntType(8))
        ])
        dtor_array_type = ir.ArrayType(dtor_struct, len(dtors))
        global_dtors = ir.GlobalVariable(self.module, dtor_array_type, name="llvm.global_dtors")
        dtor_values = [
            ir.Constant(dtor_struct, [
                ir.Constant(ir.IntType(32), prio),
                func,
                ir.Constant(ir.PointerType(ir.IntType(8)), None)
            ])
            for prio, func in dtors
        ]
        global_dtors.initializer = ir.Constant(dtor_array_type, dtor_values)
        global_dtors.linkage = 'appending'
        global_dtors.align = 8

    def get_module(self):
        return self.module
