from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Tuple

@dataclass
class OperandData:
    type: str
    register: Optional[str] = None
    immediate: Optional[Union[int, str]] = None
    size: Optional[str] = None
    base: Optional[str] = None
    index: Optional[str] = None
    scale: Optional[int] = None
    displacement: Optional[int] = None
    name: Optional[str] = None
    segment: Optional[str] = None
    relocation: Optional[str] = None
    is_rip_relative: bool = False

@dataclass
class InstructionData:
    opcode: str
    operands: List[OperandData]

@dataclass
class BlockData:
    label: str
    non_terminator_instructions: List[InstructionData]
    terminator_instruction: InstructionData

@dataclass
class FunctionData:
    name: str
    blocks: List[BlockData]

@dataclass
class SectionData:
    name: str
    alignment: int
    data: List[tuple[int, Optional[Union[int, str]], str]]
    labels: Dict[int, List[str]]

@dataclass
class ModuleData:
    sections: List[SectionData]
    functions: Dict[str, FunctionData]
    extern_symbols: List[str]
    global_symbols: List[str]
    got_symbols: List[str]
    label_to_section_offset: Dict[str, Tuple[str, int]]
