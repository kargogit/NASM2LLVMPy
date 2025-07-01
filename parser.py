from module_data import (
    OperandData,
    InstructionData,
    BlockData,
    FunctionData,
    SectionData,
    ModuleData
)
from typing import List, Dict, Any, Optional, Tuple, Union

class Parser:
    def __init__(self, json_tree: Dict[str, Any]):
        self.json_tree = json_tree
        self.extern_symbols = []
        self.global_symbols = []
        self.sections = []
        self.functions = {}
        self.current_function = None
        self.current_blocks = []
        self.got_symbols = set()
        self.call_targets = set()
        self.section_funcs = []
        self.label_to_section_offset = {}

    def parse(self) -> ModuleData:
        self.parse_symbols()
        self.parse_sections()
        self.parse_functions()
        return ModuleData(
            sections=self.sections,
            extern_symbols=self.extern_symbols,
            global_symbols=self.global_symbols,
            functions=self.functions,
            got_symbols=list(self.got_symbols),
            label_to_section_offset=self.label_to_section_offset
        )

    def parse_symbols(self):
        for entry in self.json_tree.get("program", []):

            if isinstance(entry, list):
                if not entry:
                    continue
                line_element = entry[0]
            else:

                line = entry.get("line", [])
                if not line:
                    continue
                line_element = line[0]

            if self.is_extern_directive(line_element):
                name = self.get_symbol_name(line_element)
                self.extern_symbols.append(name)
            elif self.is_global_directive(line_element):
                name = self.get_symbol_name(line_element)
                self.global_symbols.append(name)

    def parse_sections(self):
        sections = {}
        current_section = None
        current_data = []
        current_labels = {}
        offset = 0

        for entry in self.json_tree.get("program", []):
            if "line" in entry:
                line = entry["line"][0]

                if self.is_section_directive(line):
                    if current_section:
                        current_section.data.extend(current_data)
                        for label in current_labels:
                            if label in current_section.labels:
                                current_section.labels[label].extend(current_labels[label])
                            else:
                                current_section.labels[label] = current_labels[label]
                        current_data = []
                        current_labels = {}
                    name, align = self.get_section_info(line.get("directive", [{}])[1])
                    if(name in sections):
                        current_section = sections[name]
                    else:
                        offset = 0
                        current_section = SectionData(name=name, alignment=align, data=[], labels={})
                        sections[current_section.name] = current_section

                elif self.is_label(line):
                    label_name = self.get_label_name(line)
                    if label_name:
                        if offset not in current_labels:
                            current_labels[offset] = []
                        current_labels[offset].append(label_name)
                        self.label_to_section_offset[label_name] = (current_section.name, offset)

                elif self.is_data_directive(line):
                    size, value, dd_type = self.parse_data_directive(line)
                    if dd_type == "name":
                        self.section_funcs.append(value)
                    current_data.append((size, value, dd_type))
                    offset += size

        if current_section:
            current_section.data.extend(current_data)
            for label in current_labels:
                if label in current_section.labels:
                    current_section.labels[label].extend(current_labels[label])
                else:
                    current_section.labels[label] = current_labels[label]

        self.sections = list(sections.values())

    def parse_functions(self):
        functions = {}
        current_func = None
        prev_func = None
        current_blocks = []

        for entry in self.json_tree.get("program", []):
            if "block" in entry:
                for element in entry["block"]:
                    if "terminator_line" in element:
                        term = element["terminator_line"][0]
                        if "terminator_instruction" in term:
                            instr = term["terminator_instruction"][0]
                            if instr.get("terminator_opcode", [[""]])[0][0].upper() == "CALL":
                                operands = self.get_instruction_operands(term)
                                if operands and operands[0].type == "name":
                                    self.call_targets.add(operands[0].name)

        for entry in self.json_tree.get("program", []):
            if "block" in entry:
                block = entry["block"]
                label = self.get_block_label(block)
                if label == "L124f_6":
                    pass


                if label in self.global_symbols or label in self.call_targets or label in self.section_funcs:
                    if current_func:
                        if current_func == "frame_dummy":
                            current_blocks.extend(functions[prev_func].blocks[-3:])
                            functions[prev_func].blocks = functions[prev_func].blocks[:-3]
                        functions[current_func] = FunctionData(
                            name=current_func,
                            blocks=current_blocks
                        )
                        prev_func = current_func
                    current_func = label
                    current_blocks = []


                parsed_block = self.parse_block(block)
                current_blocks.append(parsed_block)


        if current_func:
            functions[current_func] = FunctionData(
                name=current_func,
                blocks=current_blocks
            )

        self.functions = functions
        for function in functions.values():
            function.parameter_regs = self._detect_parameter_registers(function)

    def _detect_parameter_registers(self, function: FunctionData) -> List[str]:
        entry_block = function.blocks[0] if function.blocks else None
        if not entry_block:
            return []

        param_regs = set()
        written_regs = set()
        sysv_regs = {'RDI', 'RSI', 'RDX', 'RCX', 'R8', 'R9'}


        write_opcodes = {
            'MOV', 'ADD', 'SUB', 'XOR', 'AND', 'OR', 'LEA', 'POP', 'INC', 'DEC',
            'SHL', 'SHR', 'SAR', 'SAL', 'SETNE', 'CDQE', 'MOVZX', 'MOVSX'
        }

        for instr in entry_block.non_terminator_instructions:
            opcode = instr.opcode.upper()


            source_ops = instr.operands if opcode in {'CMP', 'TEST'} else instr.operands[1:]
            reg_map = {
                'EDI': 'RDI', 'ESI': 'RSI', 'EDX': 'RDX', 'ECX': 'RCX',
                'R8D': 'R8', 'R9D': 'R9'
            }
            for op in source_ops:
                if op.type == 'register':
                    reg = op.register

                    reg = reg_map.get(reg, reg)
                    if reg in sysv_regs and reg not in written_regs:
                        param_regs.add(reg)


            if opcode in write_opcodes and instr.operands and instr.operands[0].type == 'register':
                reg = instr.operands[0].register
                reg = reg_map.get(reg, reg) if reg in reg_map else reg
                written_regs.add(reg)


        ordered = [reg for reg in ['RDI', 'RSI', 'RDX', 'RCX', 'R8', 'R9'] if reg in param_regs]
        return ordered

    def parse_block(self, block: List[Dict]) -> BlockData:
        label = self.get_block_label(block)
        if label == "L121f_1":
            pass
        non_term_instructions = []
        terminator_instruction = None

        for element in block:
            if "non_terminator_line" in element:
                instr = self.parse_instruction(element["non_terminator_line"][0])
                non_term_instructions.append(instr)
            elif "terminator_line" in element:
                terminator_instruction = self.parse_instruction(element["terminator_line"][0])

        return BlockData(
            label=label,
            non_terminator_instructions=non_term_instructions,
            terminator_instruction=terminator_instruction
        )

    def parse_instruction(self, instr_element: Dict) -> InstructionData:
        opcode = self.get_instruction_opcode(instr_element)
        operands = self.get_instruction_operands(instr_element)
        return InstructionData(opcode=opcode, operands=operands)

    def get_instruction_opcode(self, instr_element: Dict) -> str:
        if "instruction" in instr_element or "terminator_instruction" in instr_element:
            for part in list(instr_element.values())[0]:
                if "opcode" in part or "terminator_opcode" in part:
                    return list(part.values())[0][0][0]
        return ""

    def get_instruction_operands(self, instr_element: Dict) -> List[OperandData]:
        operands = []
        if "instruction" in instr_element or "terminator_instruction" in instr_element:
            for part in list(instr_element.values())[0]:
                if "operand" in part:
                    operand = self.parse_operand(part["operand"])
                    if operand:
                        operands.append(operand)
        return operands


    def parse_memory_expression(self, expression: List[Dict]) -> Dict:
        base = index = scale = displacement = name = segment = relocation = None
        is_rip_relative = False
        scale = 1

        for part in expression:
            if isinstance(part, dict):
                if "additiveExpression" in part:
                    addSubExpress = part["additiveExpression"]
                    if "multiplicativeExpression" in addSubExpress[0]:
                        addSubExpress = addSubExpress[0]["multiplicativeExpression"]
                        multiply = True
                    if "castExpression" in addSubExpress[0]:
                        firstOperand = addSubExpress[0]["castExpression"][0]
                        if "register" in firstOperand:
                            base = firstOperand["register"][0][0]
                        elif "name" in firstOperand:
                            name = firstOperand["name"][0][0]
                            name = name.replace("RELA", "L")
                        if "castExpression" in addSubExpress[2]:
                            secondOperand = addSubExpress[2]["castExpression"][0]
                            if "integer" in secondOperand:
                                sign = addSubExpress[1][0]
                                if sign in ['+', '-']:
                                    int_str = secondOperand["integer"][0][0]
                                    num_base = 16 if int_str.startswith("0x") else 10
                                    value = int(int_str, num_base)
                                    displacement = value if sign == '+' else -value
                                elif sign == '*':
                                    scale = int(secondOperand["integer"][0][0], 16 if "0x" in secondOperand["integer"][0][0] else 10)
                if "castExpression" in part:
                    castExpression = part["castExpression"][0]
                    if "name" in castExpression:
                        name = castExpression["name"][0][0]
                    elif "register" in castExpression:
                        base = castExpression["register"][0][0]
                elif "segment" in part:
                    segment = part["segment"][0][0][0]
                elif "register" in part:
                    reg = part["register"][0][0][0]
                    if reg == "RIP":
                        is_rip_relative = True
                    if not base:
                        base = reg
                    elif not index:
                        index = reg
                elif "scaled_register" in part:
                    index = part["scaled_register"]["register"][0][0][0]
                    scale = int(part["scaled_register"]["scale"][0][0])
                elif "integer" in part:
                    disp = part["integer"][0][0]
                    displacement = int(disp, 16 if disp.startswith("0x") else 10)
                elif "wrt" in part:

                    name = part["wrt"][0]["name"][0][0]
                    relocation = part["wrt"][2][0]

        if name is not None and base is None and index is None and relocation is None:
            is_rip_relative = True

        return {
            "base": base, "index": index, "scale": scale,
            "displacement": displacement, "name": name,
            "segment": segment, "relocation": relocation,
            "is_rip_relative": is_rip_relative
        }

    def parse_operand(self, operand_parts: List[Dict]) -> Optional[OperandData]:
        operand = OperandData(type="unknown")
        size = register = immediate = name = None

        for part in operand_parts:
            if isinstance(part, dict):
                if "size" in part:
                    size = part["size"][0][0]
                elif "register" in part:
                    register = part["register"][0][0]
                elif "integer" in part:
                    int_str = part["integer"][0][0]
                    immediate = int(int_str, 16 if int_str.startswith("0x") else 10)
                elif "expression" in part:
                    mem_expr = self.parse_memory_expression(part["expression"])
                    operand.size = size
                    if mem_expr["relocation"]:
                        operand.type = "name"
                        operand.name = mem_expr["name"]
                        operand.relocation = mem_expr["relocation"]

                        if mem_expr["relocation"] == "..got" and mem_expr["name"]:
                            self.got_symbols.add(mem_expr["name"])
                    else:
                        operand.type = "memory"
                        operand.__dict__.update({k: mem_expr[k] for k in [
                            "base", "index", "scale", "displacement", "name", "segment", "is_rip_relative"
                        ]})
                elif "name" in part:
                    name = part["name"][0][0]

        if register:
            operand.type = "register"
            operand.register = register
        elif immediate is not None:
            operand.type = "immediate"
            operand.immediate = immediate
        elif name:
            operand.type = "name"
            operand.name = name

        return operand if operand.type != "unknown" else None


    def is_extern_directive(self, line: Dict) -> bool:
        return self.has_directive_type(line, "extern")

    def is_global_directive(self, line: Dict) -> bool:
        return self.has_directive_type(line, "global")

    def has_directive_type(self, line: Dict, directive_type: str) -> bool:
        if "directive" in line:
            for part in line["directive"]:
                if directive_type in part:
                    return True
        return False

    def get_symbol_name(self, line: Dict) -> str:
        for part in line.get("directive", []):
            if isinstance(part, dict):
                if "extern_params" in part:
                    return part["extern_params"][0]["name"][0][0]
                if "global_params" in part:
                    return part["global_params"][0]["name"][0][0]
        return ""

    def is_section_directive(self, line: Dict) -> bool:
        return "section" in line.get("directive", [{}])[0]

    def get_section_info(self, line: Dict) -> Tuple[str, int]:
        name = ""
        align = 1

        for part in line.get("section_params", []):
            if "name" in part:
                name = part["name"][0][0]
            elif "alignment" in part:
                align = int(part["alignment"][2]["integer"][0][0])

        return name, align

    def is_label(self, line: Dict) -> bool:
        return "label" in line

    def get_label_name(self, line: Dict) -> str:
        return line.get("label", [{}])[0].get("name", [[[""]]])[0][0]

    def is_data_directive(self, line: Dict) -> bool:
        return "pseudoinstruction" in line


    def parse_data_directive(self, line: Dict) -> Tuple[int, Optional[Union[int, str]]]:

        define_sizes = {
            "db": 1,
            "dw": 2,
            "dd": 4,
            "dq": 8,
            "dt": 10
        }

        reserve_sizes = {
            "resb": 1,
            "resw": 2,
            "resd": 4,
            "resq": 8,
            "rest": 10
        }


        pseudo_instr = line.get("pseudoinstruction", [{}])
        if not pseudo_instr or not isinstance(pseudo_instr, list):
            return 0, None

        directive_type = (
            "dx" if "dx" in pseudo_instr[0]
            else "resx" if "resx" in pseudo_instr[0]
            else "None"
        )
        directive_type = pseudo_instr[0].get(directive_type, [])
        if not directive_type or not isinstance(directive_type, list) or not directive_type[0]:
            return 0, None, None


        if isinstance(directive_type[0], dict):

            directive = next(iter(directive_type[0].keys()), "").lower()
        elif isinstance(directive_type[0], list):

            directive = str(directive_type[0][0]).lower()
        else:
            directive = str(directive_type[0]).lower()


        if directive in define_sizes:
            size = define_sizes[directive]
            value_part = pseudo_instr[1].get("value", [{}])
            atom = value_part[0].get("atom", [{}])

            if not atom[0]:
                return size, None, None

            if "integer" in atom[0]:
                val = atom[0]["integer"][0][0]

                if val.endswith("h"):
                    val = int(val[:-1], 16)
                else:
                    val = int(val, 10)
                return size, val, "integer"
            elif "name" in atom[0]:
                name = atom[0]["name"][0][0]
                return size, name, "name"
            elif "string" in atom[0]:
                return len(atom[0]["string"][0][0]) - 2, atom[0]["string"][0][0][1:-1], "string"
            elif "float" in atom[0] and directive == "dt":
                return size, float(atom["float"][0][0]), "float"

            return size, None, None


        elif directive in reserve_sizes:
            item_size = reserve_sizes[directive]
            count = int(pseudo_instr[1].get("integer", [[0]])[0][0])
            total_size = count * item_size
            return total_size, None, "integer"


        return 0, None, None

    def get_block_label(self, block: List[Dict]) -> str:
        for part in block:
            if "label" in part:
                label = part["label"][0]["name"][0][0]
                if not label or label == "_":
                    return f"L{hash(str(block))}"
                return label
        return f"L{hash(str(block))}"
