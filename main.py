import json
from parser import Parser
from module_data import ModuleData
from llvm_generator import LLVMGenerator
from function_translator import FunctionTranslator
import sys
#builder.add(ir.Constant(ir.IntType(1), 0), ir.Constant(ir.IntType(1), 0), name="nop14")

def main():

    if len(sys.argv) < 2:
        print("Usage: python3 main.py <input_asm_file>")
        sys.exit(1)

    input_filename = sys.argv[1]

    try:
        with open(input_filename, "r") as file:
            json_tree = json.load(file)
    except FileNotFoundError:
        print("Error: 'assembly.json' not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in 'assembly.json'.")
        return
    parser = Parser(json_tree)
    module_data: ModuleData = parser.parse()

    llvm_generator = LLVMGenerator(
        module_name="lifted_module",
        target_triple="x86_64-pc-linux-gnu"
    )
    function_translator = FunctionTranslator(llvm_generator)
    function_translator.declare_all_functions(module_data)

    llvm_module = llvm_generator.generate(module_data)

    function_translator.translate_all_functions(module_data)

    '''
    try:
        verify_module(llvm_module)
        print("LLVM IR verification successful.")
    except Exception as e:
        print(f"LLVM IR verification failed: {str(e)}")
        return
    '''

    print(llvm_module)
if __name__ == "__main__":
    main()
