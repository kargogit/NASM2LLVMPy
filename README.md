# NASM2LLVMPy
Assembly to LLVM IR lifter for x86-64 ELF Executables

# Steps: </br>
antlr4 -Dlanguage=Python3 nasm_x86_64_Lexer.g4 </br>
antlr4 -Dlanguage=Python3 nasm_x86_64_Parser.g4 </br>
python3 asmParser.py wc.asm </br>
python3 main.py wc.json
