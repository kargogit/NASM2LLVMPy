extern _ITM_deregisterTMCloneTable
extern _ITM_registerTMCloneTable
extern __cxa_atexit
extern __cxa_finalize
extern __errno_location
extern __gmon_start__
extern __libc_start_main
extern __stack_chk_fail
extern exit
extern fclose
extern fprintf
extern fputc
extern fwrite
extern geteuid
extern getopt_long
extern getpwuid
extern malloc
extern optind
extern printf
extern puts
extern setlocale
extern stderr
extern stdout
extern strcpy
extern strerror
extern strlen
extern strrchr
extern vfprintf


global _IO_stdin_used
global __TMC_END__
global __bss_start
global __data_start
global __dso_handle
global _edata
global _end
global _fini
global _init
global _start
global close_stdout
global emit_ancillary_info
global emit_try_help
global error
global initialize_main
global main
global parse_gnu_standard_options_only
global proper_name
global quote
global set_program_name
global usage


default rel


; ---------------
; Function: _init
; ---------------
; Entry 1000; block 0; address 1000
_init:
  SUB RSP, 0x8
  MOV qword [Ltemp_storage_foxdec], RBX ; inserted
  LEA RBX, [__gmon_start__ wrt ..plt]
  MOV RAX, RBX
  MOV RBX, qword [Ltemp_storage_foxdec] ; inserted
  TEST RAX, RAX
  JZ L1000_2    ; 0x1016 --> L1000_2

; Entry 1000; block 1; address 1014
L1000_1:
  ; Resolved indirection: RAX --> __gmon_start__
  CALL __gmon_start__ wrt ..plt

; Entry 1000; block 2; address 1016
L1000_2:
  ADD RSP, 0x8
  RET




; ----------------
; Function: _start
; ----------------
; Entry 12c0; block 0; address 12c0
_start:
  XOR EBP, EBP
  MOV R9, RDX
  POP RSI
  MOV RDX, RSP
  AND RSP, 0xfffffffffffffff0
  PUSH RAX
  PUSH RSP
  XOR R8D, R8D
  XOR ECX, ECX
  LEA RDI, [main]    ; 0x1843 --> main
  CALL __libc_start_main wrt ..plt

; Entry 12c0; block 1; address 12e5
L12c0_1:
  HLT




; ------------------------------
; Function: deregister_tm_clones
; ------------------------------
; Entry 12f0; block 0; address 12f0
deregister_tm_clones:
  LEA RDI, [stdout]    ; 0x4080 --> stdout
  LEA RAX, [stdout]    ; 0x4080 --> stdout
  CMP RAX, RDI
  JZ L12f0_2    ; 0x1318 --> L12f0_2

; Entry 12f0; block 1; address 1303
L12f0_1:
  MOV qword [Ltemp_storage_foxdec], RBX ; inserted
  LEA RBX, [_ITM_deregisterTMCloneTable wrt ..plt]
  MOV RAX, RBX
  MOV RBX, qword [Ltemp_storage_foxdec] ; inserted
  TEST RAX, RAX
  JZ L12f0_2    ; 0x1318 --> L12f0_2

; Entry 12f0; block 3; address 130f
L12f0_3:
  ; Resolved indirection: RAX --> _ITM_deregisterTMCloneTable
  JMP _ITM_deregisterTMCloneTable wrt ..plt

; Entry 12f0; block 2; address 1318
L12f0_2:
  RET




; -------------------------------
; Function: __do_global_dtors_aux
; -------------------------------
; Entry 1360; block 0; address 1360
__do_global_dtors_aux:
  CMP byte [L_.bss_0x40a8], 0x0    ; 0x40a8 --> L_.bss_0x40a8
  JNZ L1360_2    ; 0x1398 --> L1360_2

; Entry 1360; block 1; address 136d
L1360_1:
  PUSH RBP
  MOV qword [Ltemp_storage_foxdec], RAX ; inserted
  LEA RAX, [__cxa_finalize wrt ..plt]
  CMP RAX, 0x0
  MOV RAX, qword [Ltemp_storage_foxdec] ; inserted
  MOV RBP, RSP
  JZ L1360_4    ; 0x1387 --> L1360_4

; Entry 1360; block 3; address 137b
L1360_3:
  MOV RDI, qword [__dso_handle]    ; 0x4008 --> __dso_handle
  CALL __cxa_finalize wrt ..plt

; Entry 1360; block 4; address 1387
L1360_4:
  CALL deregister_tm_clones    ; 0x12f0 --> deregister_tm_clones

; Entry 1360; block 5; address 138c
L1360_5:
  MOV byte [L_.bss_0x40a8], 0x1    ; 0x40a8 --> L_.bss_0x40a8
  POP RBP
  RET

; Entry 1360; block 2; address 1398
L1360_2:
  RET




; ---------------------
; Function: frame_dummy
; ---------------------
; Entry 13a0; block 1; address 1344
L13a0_1:
  MOV qword [Ltemp_storage_foxdec], RBX ; inserted
  LEA RBX, [_ITM_registerTMCloneTable wrt ..plt]
  MOV RAX, RBX
  MOV RBX, qword [Ltemp_storage_foxdec] ; inserted
  TEST RAX, RAX
  JZ L13a0_2    ; 0x1358 --> L13a0_2

; Entry 13a0; block 3; address 1350
L13a0_3:
  ; Resolved indirection: RAX --> _ITM_registerTMCloneTable
  JMP _ITM_registerTMCloneTable wrt ..plt

; Entry 13a0; block 2; address 1358
L13a0_2:
  RET

; Entry 13a0; block 0; address 13a0
frame_dummy:
  LEA RDI, [stdout]    ; 0x4080 --> stdout
  LEA RSI, [stdout]    ; 0x4080 --> stdout
  SUB RSI, RDI
  MOV RAX, RSI
  SHR RSI, 0x3f
  SAR RAX, 0x3
  ADD RSI, RAX
  SAR RSI, 0x1
  JZ L13a0_2    ; 0x1358 --> L13a0_2
  JMP L13a0_1 ; jump is inserted




; ---------------
; Function: quote
; ---------------
; Entry 13a9; block 0; address 13a9
quote:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x20
  MOV qword [RBP - 0x18], RDI
  CMP qword [RBP - 0x18], 0x0
  JNZ L13a9_2    ; 0x13c7 --> L13a9_2

; Entry 13a9; block 1; address 13c0
L13a9_1:
  MOV EAX, 0x0
  JMP L13a9_7    ; 0x1401 --> L13a9_7

; Entry 13a9; block 2; address 13c7
L13a9_2:
  MOV RAX, qword [RBP - 0x18]
  MOV RDI, RAX
  CALL strlen wrt ..plt

; Entry 13a9; block 3; address 13d3
L13a9_3:
  ADD RAX, 0x1
  MOV RDI, RAX
  CALL malloc wrt ..plt

; Entry 13a9; block 4; address 13df
L13a9_4:
  MOV qword [RBP - 0x8], RAX
  CMP qword [RBP - 0x8], 0x0
  JZ L13a9_6    ; 0x13fd --> L13a9_6

; Entry 13a9; block 5; address 13ea
L13a9_5:
  MOV RDX, qword [RBP - 0x18]
  MOV RAX, qword [RBP - 0x8]
  MOV RSI, RDX
  MOV RDI, RAX
  CALL strcpy wrt ..plt

; Entry 13a9; block 6; address 13fd
L13a9_6:
  MOV RAX, qword [RBP - 0x8]

; Entry 13a9; block 7; address 1401
L13a9_7:
  LEAVE
  RET




; ---------------
; Function: error
; ---------------
; Entry 1403; block 0; address 1403
error:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0xe0
  MOV dword [RBP - 0xd4], EDI
  MOV dword [RBP - 0xd8], ESI
  MOV qword [RBP - 0xe0], RDX
  MOV qword [RBP - 0x98], RCX
  MOV qword [RBP - 0x90], R8
  MOV qword [RBP - 0x88], R9
  TEST AL, AL
  JZ L1403_2    ; 0x145e --> L1403_2

; Entry 1403; block 1; address 143e
L1403_1:
  MOVAPS oword [RBP - 0x80], XMM0
  MOVAPS oword [RBP - 0x70], XMM1
  MOVAPS oword [RBP - 0x60], XMM2
  MOVAPS oword [RBP - 0x50], XMM3
  MOVAPS oword [RBP - 0x40], XMM4
  MOVAPS oword [RBP - 0x30], XMM5
  MOVAPS oword [RBP - 0x20], XMM6
  MOVAPS oword [RBP - 0x10], XMM7

; Entry 1403; block 2; address 145e
L1403_2:
  MOV RAX, qword [FS + 0x28]
  MOV qword [RBP - 0xb8], RAX
  XOR EAX, EAX
  MOV RDX, qword [L_.bss_0x40b0]    ; 0x40b0 --> L_.bss_0x40b0
  MOV RAX, qword [stderr]    ; 0x40a0 --> stderr
  LEA RCX, [L_.rodata_0x2008]    ; 0x2008 --> L_.rodata_0x2008
  MOV RSI, RCX
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL fprintf wrt ..plt

; Entry 1403; block 3; address 1495
L1403_3:
  MOV dword [RBP - 0xd0], 0x18
  MOV dword [RBP - 0xcc], 0x30
  LEA RAX, [RBP + 0x10]
  MOV qword [RBP - 0xc8], RAX
  LEA RAX, [RBP - 0xb0]
  MOV qword [RBP - 0xc0], RAX
  MOV RAX, qword [stderr]    ; 0x40a0 --> stderr
  LEA RDX, [RBP - 0xd0]
  MOV RCX, qword [RBP - 0xe0]
  MOV RSI, RCX
  MOV RDI, RAX
  CALL vfprintf wrt ..plt

; Entry 1403; block 4; address 14e2
L1403_4:
  CMP dword [RBP - 0xd8], 0x0
  JZ L1403_6    ; 0x1519 --> L1403_6

; Entry 1403; block 5; address 14eb
L1403_5:
  MOV EAX, dword [RBP - 0xd8]
  MOV EDI, EAX
  CALL strerror wrt ..plt

; Entry 1403; block 7; address 14f8
L1403_7:
  MOV RDX, RAX
  MOV RAX, qword [stderr]    ; 0x40a0 --> stderr
  LEA RCX, [L_.rodata_0x200d]    ; 0x200d --> L_.rodata_0x200d
  MOV RSI, RCX
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL fprintf wrt ..plt

; Entry 1403; block 6; address 1519
L1403_6:
  MOV RAX, qword [stderr]    ; 0x40a0 --> stderr
  MOV RSI, RAX
  MOV EDI, 0xa
  CALL fputc wrt ..plt

; Entry 1403; block 8; address 152d
L1403_8:
  CMP dword [RBP - 0xd4], 0x0
  JZ L1403_10    ; 0x1543 --> L1403_10

; Entry 1403; block 9; address 1536
L1403_9:
  MOV EAX, dword [RBP - 0xd4]
  MOV EDI, EAX
  NOP
FOXDEC_TERMINATING_L1403_9:
  CALL exit wrt ..plt

; Entry 1403; block 10; address 1543
L1403_10:
  MOV RAX, qword [RBP - 0xb8]
  SUB RAX, qword [FS + 0x28]
  JZ L1403_12    ; 0x155b --> L1403_12

; Entry 1403; block 11; address 1556
L1403_11:
  NOP
FOXDEC_TERMINATING_L1403_11:
  CALL __stack_chk_fail wrt ..plt

; Entry 1403; block 12; address 155b
L1403_12:
  LEAVE
  RET




; --------------------------
; Function: set_program_name
; --------------------------
; Entry 155d; block 0; address 155d
set_program_name:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x20
  MOV qword [RBP - 0x18], RDI
  MOV RAX, qword [RBP - 0x18]
  MOV qword [L_.bss_0x40b0], RAX    ; 0x40b0 --> L_.bss_0x40b0
  MOV RAX, qword [L_.bss_0x40b0]    ; 0x40b0 --> L_.bss_0x40b0
  MOV ESI, 0x2f
  MOV RDI, RAX
  CALL strrchr wrt ..plt

; Entry 155d; block 1; address 158c
L155d_1:
  MOV qword [RBP - 0x8], RAX
  CMP qword [RBP - 0x8], 0x0
  JZ L155d_3    ; 0x15a6 --> L155d_3

; Entry 155d; block 2; address 1597
L155d_2:
  MOV RAX, qword [RBP - 0x8]
  ADD RAX, 0x1
  MOV qword [L_.bss_0x40b0], RAX    ; 0x40b0 --> L_.bss_0x40b0

; Entry 155d; block 3; address 15a6
L155d_3:
  LEAVE
  RET




; -------------------------
; Function: initialize_main
; -------------------------
; Entry 15a9; block 0; address 15a9
initialize_main:
  PUSH RBP
  MOV RBP, RSP
  MOV qword [RBP - 0x8], RDI
  MOV qword [RBP - 0x10], RSI
  POP RBP
  RET




; ----------------------
; Function: close_stdout
; ----------------------
; Entry 15bc; block 0; address 15bc
close_stdout:
  PUSH RBP
  MOV RBP, RSP
  MOV RAX, qword [stdout]    ; 0x4080 --> stdout
  MOV RDI, RAX
  CALL fclose wrt ..plt

; Entry 15bc; block 1; address 15d3
L15bc_1:
  TEST EAX, EAX
  JZ L15bc_3    ; 0x1620 --> L15bc_3

; Entry 15bc; block 2; address 15d7
L15bc_2:
  CALL __errno_location wrt ..plt

; Entry 15bc; block 4; address 15dc
L15bc_4:
  MOV EAX, dword [RAX]
  CMP EAX, 0x20
  JZ L15bc_3    ; 0x1620 --> L15bc_3

; Entry 15bc; block 5; address 15e3
L15bc_5:
  CALL __errno_location wrt ..plt

; Entry 15bc; block 6; address 15e8
L15bc_6:
  MOV EAX, dword [RAX]
  MOV EDI, EAX
  CALL strerror wrt ..plt

; Entry 15bc; block 7; address 15f1
L15bc_7:
  MOV RCX, RAX
  MOV RDX, qword [L_.bss_0x40b0]    ; 0x40b0 --> L_.bss_0x40b0
  MOV RAX, qword [stderr]    ; 0x40a0 --> stderr
  LEA RSI, [L_.rodata_0x2012]    ; 0x2012 --> L_.rodata_0x2012
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL fprintf wrt ..plt

; Entry 15bc; block 8; address 1616
L15bc_8:
  MOV EDI, 0x1
  NOP
FOXDEC_TERMINATING_L15bc_8:
  CALL exit wrt ..plt

; Entry 15bc; block 3; address 1620
L15bc_3:
  POP RBP
  RET




; -----------------------
; Function: emit_try_help
; -----------------------
; Entry 1623; block 0; address 1623
emit_try_help:
  PUSH RBP
  MOV RBP, RSP
  MOV RDX, qword [L_.bss_0x40b0]    ; 0x40b0 --> L_.bss_0x40b0
  MOV RAX, qword [stderr]    ; 0x40a0 --> stderr
  LEA RCX, [L_.rodata_0x2030]    ; 0x2030 --> L_.rodata_0x2030
  MOV RSI, RCX
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL fprintf wrt ..plt

; Entry 1623; block 1; address 1650
L1623_1:
  POP RBP
  RET




; -----------------------------
; Function: emit_ancillary_info
; -----------------------------
; Entry 1653; block 0; address 1653
emit_ancillary_info:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x10
  MOV qword [RBP - 0x8], RDI
  LEA RAX, [L_.rodata_0x2058]    ; 0x2058 --> L_.rodata_0x2058
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 1653; block 1; address 1672
L1653_1:
  MOV RAX, qword [RBP - 0x8]
  MOV RDX, RAX
  LEA RAX, [L_.rodata_0x207f]    ; 0x207f --> L_.rodata_0x207f
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2090]    ; 0x2090 --> L_.rodata_0x2090
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1653; block 2; address 1697
L1653_2:
  LEA RAX, [L_.rodata_0x20c8]    ; 0x20c8 --> L_.rodata_0x20c8
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 1653; block 3; address 16a6
L1653_3:
  LEAVE
  RET




; ---------------------
; Function: proper_name
; ---------------------
; Entry 16a9; block 0; address 16a9
proper_name:
  PUSH RBP
  MOV RBP, RSP
  MOV qword [RBP - 0x8], RDI
  MOV RAX, qword [RBP - 0x8]
  POP RBP
  RET




; -----------------------------------------
; Function: parse_gnu_standard_options_only
; -----------------------------------------
; Entry 16bb; block 0; address 16bb
parse_gnu_standard_options_only:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x40
  MOV dword [RBP - 0x14], EDI
  MOV qword [RBP - 0x20], RSI
  MOV qword [RBP - 0x28], RDX
  MOV qword [RBP - 0x30], RCX
  MOV qword [RBP - 0x38], R8
  MOV dword [RBP - 0x18], R9D
  JMP L16bb_7    ; 0x174e --> L16bb_7

; Entry 16bb; block 10; address 16e0
L16bb_10:
  CMP dword [RBP - 0x4], 0x68
  JZ L16bb_3    ; 0x16ee --> L16bb_3

; Entry 16bb; block 2; address 16e6
L16bb_2:
  CMP dword [RBP - 0x4], 0x76
  JZ L16bb_5    ; 0x16fb --> L16bb_5

; Entry 16bb; block 4; address 16ec
L16bb_4:
  MOV RAX, qword [RBP + 0x10]
  MOV EDI, 0x1
  CALL RAX
  ; Unresolved indirection
  JMP L16bb_7 ; jump is inserted

; Entry 16bb; block 3; address 16ee
L16bb_3:
  MOV RAX, qword [RBP + 0x10]
  MOV EDI, 0x0
  CALL RAX
  ; Unresolved indirection

; Entry 16bb; block 6; address 16f9
L16bb_6:
  JMP L16bb_7    ; 0x174e --> L16bb_7

; Entry 16bb; block 5; address 16fb
L16bb_5:
  MOV RCX, qword [RBP - 0x38]
  MOV RDX, qword [RBP - 0x30]
  MOV RAX, qword [RBP - 0x28]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2108]    ; 0x2108 --> L_.rodata_0x2108
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 16bb; block 8; address 171e
L16bb_8:
  MOV RAX, qword [RBP + 0x18]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2114]    ; 0x2114 --> L_.rodata_0x2114
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 16bb; block 9; address 1739
L16bb_9:
  MOV EDI, 0x0
  NOP
FOXDEC_TERMINATING_L16bb_9:
  CALL exit wrt ..plt
L16bb_9_HLT:
  HLT ; should never be reached    ; 0x1743 --> L16bb_9_HLT

; Entry 16bb; block 7; address 174e
L16bb_7:
  MOV RSI, qword [RBP - 0x20]
  MOV EAX, dword [RBP - 0x14]
  MOV R8D, 0x0
  LEA RDX, [L_reloc_0x4020_0x2251]    ; 0x4020 --> L_reloc_0x4020_0x2251
  MOV RCX, RDX
  LEA RDX, [L_.rodata_0x2124]    ; 0x2124 --> L_.rodata_0x2124
  MOV EDI, EAX
  CALL getopt_long wrt ..plt

; Entry 16bb; block 1; address 1773
L16bb_1:
  MOV dword [RBP - 0x4], EAX
  CMP dword [RBP - 0x4], 0xffffffff
  JNZ L16bb_10    ; 0x16e0 --> L16bb_10

; Entry 16bb; block 11; address 1780
L16bb_11:
  LEAVE
  RET




; ---------------
; Function: usage
; ---------------
; Entry 1784; block 0; address 1784
usage:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x10
  MOV dword [RBP - 0x4], EDI
  CMP dword [RBP - 0x4], 0x0
  JZ L1784_2    ; 0x17a3 --> L1784_2

; Entry 1784; block 1; address 1799
L1784_1:
  CALL emit_try_help    ; 0x1623 --> emit_try_help

; Entry 1784; block 3; address 179e
L1784_3:
  JMP L1784_8    ; 0x1839 --> L1784_8

; Entry 1784; block 2; address 17a3
L1784_2:
  MOV RAX, qword [L_.bss_0x40b0]    ; 0x40b0 --> L_.bss_0x40b0
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2125]    ; 0x2125 --> L_.rodata_0x2125
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1784; block 4; address 17c1
L1784_4:
  MOV RAX, qword [stdout]    ; 0x4080 --> stdout
  MOV RCX, RAX
  MOV EDX, 0x54
  MOV ESI, 0x1
  LEA RAX, [L_.rodata_0x2140]    ; 0x2140 --> L_.rodata_0x2140
  MOV RDI, RAX
  CALL fwrite wrt ..plt

; Entry 1784; block 5; address 17e4
L1784_5:
  MOV RAX, qword [stdout]    ; 0x4080 --> stdout
  MOV RCX, RAX
  MOV EDX, 0x2c
  MOV ESI, 0x1
  LEA RAX, [L_.rodata_0x2198]    ; 0x2198 --> L_.rodata_0x2198
  MOV RDI, RAX
  CALL fwrite wrt ..plt

; Entry 1784; block 6; address 1807
L1784_6:
  MOV RAX, qword [stdout]    ; 0x4080 --> stdout
  MOV RCX, RAX
  MOV EDX, 0x35
  MOV ESI, 0x1
  LEA RAX, [L_.rodata_0x21c8]    ; 0x21c8 --> L_.rodata_0x21c8
  MOV RDI, RAX
  CALL fwrite wrt ..plt

; Entry 1784; block 7; address 182a
L1784_7:
  LEA RAX, [L_.rodata_0x21fe]    ; 0x21fe --> L_.rodata_0x21fe
  MOV RDI, RAX
  CALL emit_ancillary_info    ; 0x1653 --> emit_ancillary_info

; Entry 1784; block 8; address 1839
L1784_8:
  MOV EAX, dword [RBP - 0x4]
  MOV EDI, EAX
  NOP
FOXDEC_TERMINATING_L1784_8:
  CALL exit wrt ..plt




; --------------
; Function: main
; --------------
; Entry 1843; block 0; address 1843
main:
  PUSH RBP
  MOV RBP, RSP
  PUSH RBX
  SUB RSP, 0x28
  MOV dword [RBP - 0x24], EDI
  MOV qword [RBP - 0x30], RSI
  MOV dword [RBP - 0x20], 0xffffffff
  LEA RDX, [RBP - 0x30]
  LEA RAX, [RBP - 0x24]
  MOV RSI, RDX
  MOV RDI, RAX
  CALL initialize_main    ; 0x15a9 --> initialize_main

; Entry 1843; block 1; address 1871
L1843_1:
  MOV RAX, qword [RBP - 0x30]
  MOV RAX, qword [RAX]
  MOV RDI, RAX
  CALL set_program_name    ; 0x155d --> set_program_name

; Entry 1843; block 2; address 1880
L1843_2:
  LEA RAX, [L_.rodata_0x2124]    ; 0x2124 --> L_.rodata_0x2124
  MOV RSI, RAX
  MOV EDI, 0x6
  CALL setlocale wrt ..plt

; Entry 1843; block 3; address 1894
L1843_3:
  LEA RAX, [close_stdout]    ; 0x15bc --> close_stdout
  MOV RDI, RAX
  CALL atexit    ; 0x19d0 --> atexit

; Entry 1843; block 4; address 18a3
L1843_4:
  LEA RAX, [L_.rodata_0x2205]    ; 0x2205 --> L_.rodata_0x2205
  MOV RDI, RAX
  CALL proper_name    ; 0x16a9 --> proper_name

; Entry 1843; block 5; address 18b2
L1843_5:
  MOV RDX, RAX
  MOV RSI, qword [RBP - 0x30]
  MOV EAX, dword [RBP - 0x24]
  SUB RSP, 0x8
  PUSH 0x0
  PUSH RDX
  LEA RDX, [usage]    ; 0x1784 --> usage
  PUSH RDX
  MOV R9D, 0x1
  LEA R8, [L_.rodata_0x2216]    ; 0x2216 --> L_.rodata_0x2216
  LEA RDX, [L_.rodata_0x207f]    ; 0x207f --> L_.rodata_0x207f
  MOV RCX, RDX
  LEA RDX, [L_.rodata_0x21fe]    ; 0x21fe --> L_.rodata_0x21fe
  MOV EDI, EAX
  CALL parse_gnu_standard_options_only    ; 0x16bb --> parse_gnu_standard_options_only

; Entry 1843; block 6; address 18f0
L1843_6:
  ADD RSP, 0x20
  MOV EDX, dword [optind]    ; 0x4088 --> optind
  MOV EAX, dword [RBP - 0x24]
  CMP EDX, EAX
  JZ L1843_8    ; 0x194b --> L1843_8

; Entry 1843; block 7; address 1901
L1843_7:
  MOV RAX, qword [RBP - 0x30]
  MOV EDX, dword [optind]    ; 0x4088 --> optind
  MOVSXD RDX, EDX
  SHL RDX, 0x3
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  MOV RDI, RAX
  CALL quote    ; 0x13a9 --> quote

; Entry 1843; block 9; address 1920
L1843_9:
  MOV RCX, RAX
  LEA RAX, [L_.rodata_0x221a]    ; 0x221a --> L_.rodata_0x221a
  MOV RDX, RAX
  MOV ESI, 0x0
  MOV EDI, 0x0
  MOV EAX, 0x0
  CALL error    ; 0x1403 --> error

; Entry 1843; block 10; address 1941
L1843_10:
  MOV EDI, 0x1
  NOP
FOXDEC_TERMINATING_L1843_10:
  CALL usage    ; 0x1784 --> usage

; Entry 1843; block 8; address 194b
L1843_8:
  CALL __errno_location wrt ..plt

; Entry 1843; block 11; address 1950
L1843_11:
  MOV dword [RAX], 0x0
  CALL geteuid wrt ..plt

; Entry 1843; block 12; address 195b
L1843_12:
  MOV dword [RBP - 0x1c], EAX
  MOV EAX, dword [RBP - 0x1c]
  CMP EAX, dword [RBP - 0x20]
  JNZ L1843_14    ; 0x1971 --> L1843_14

; Entry 1843; block 13; address 1966
L1843_13:
  CALL __errno_location wrt ..plt

; Entry 1843; block 15; address 196b
L1843_15:
  MOV EAX, dword [RAX]
  TEST EAX, EAX
  JNZ L1843_16    ; 0x197d --> L1843_16

; Entry 1843; block 14; address 1971
L1843_14:
  MOV EAX, dword [RBP - 0x1c]
  MOV EDI, EAX
  CALL getpwuid wrt ..plt

; Entry 1843; block 17; address 197b
L1843_17:
  JMP L1843_18    ; 0x1982 --> L1843_18

; Entry 1843; block 16; address 197d
L1843_16:
  MOV EAX, 0x0

; Entry 1843; block 18; address 1982
L1843_18:
  MOV qword [RBP - 0x18], RAX
  CMP qword [RBP - 0x18], 0x0
  JNZ L1843_20    ; 0x19b2 --> L1843_20

; Entry 1843; block 19; address 198d
L1843_19:
  MOV EBX, dword [RBP - 0x1c]
  CALL __errno_location wrt ..plt

; Entry 1843; block 21; address 1995
L1843_21:
  MOV EAX, dword [RAX]
  MOV RCX, RBX
  LEA RDX, [L_.rodata_0x2230]    ; 0x2230 --> L_.rodata_0x2230
  MOV ESI, EAX
  MOV EDI, 0x1
  MOV EAX, 0x0
  CALL error    ; 0x1403 --> error

; Entry 1843; block 20; address 19b2
L1843_20:
  MOV RAX, qword [RBP - 0x18]
  MOV RAX, qword [RAX]
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 1843; block 22; address 19c1
L1843_22:
  MOV EAX, 0x0
  MOV RBX, qword [RBP - 0x8]
  LEAVE
  RET




; ----------------
; Function: atexit
; ----------------
; Entry 19d0; block 0; address 19d0
atexit:
  MOV RDX, qword [__dso_handle]    ; 0x4008 --> __dso_handle
  XOR ESI, ESI
  JMP __cxa_atexit wrt ..plt




; ---------------
; Function: _fini
; ---------------
; Entry 19e4; block 0; address 19e4
_fini:
  SUB RSP, 0x8
  ADD RSP, 0x8
  RET




section .rodata align=8 ; @2000
L_.rodata_0x2000:
db 01h
db 00h
db 02h
db 00h
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x2008:
db "%s: ", 0; @ 2008
L_.rodata_0x200d:
db ": %s", 0; @ 200d
L_.rodata_0x2012:
db "%s: error writing output: %s\n", 0; @ 2012
L_.rodata_0x2030:
db "Try '%s --help' for more information.\n", 0; @ 2030
db 00h
L_.rodata_0x2058:
db "\nReport bugs to: bug-coreutils@gnu.org", 0; @ 2058
L_.rodata_0x207f:
db "coreutils", 0; @ 207f
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x2090:
db "%s home page: <https://www.gnu.org/software/%s/>\n", 0; @ 2090
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x20c8:
db "General help using GNU software: <https://www.gnu.org/gethelp/>", 0; @ 20c8
L_.rodata_0x2108:
db "%s (%s) %s\n", 0; @ 2108
L_.rodata_0x2114:
db "Written by %s.\n", 0; @ 2114
L_.rodata_0x2124:
db 00h
L_.rodata_0x2125:
db "Usage: %s [OPTION]...\n", 0; @ 2125
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x2140:
db "Print the user name associated with the current effective user ID.\nSame as id -un.\n\n", 0; @ 2140
db 00h
db 00h
db 00h
L_.rodata_0x2198:
db "      --help     display this help and exit\n", 0; @ 2198
db 00h
db 00h
db 00h
L_.rodata_0x21c8:
db "      --version  output version information and exit\n", 0; @ 21c8
L_.rodata_0x21fe:
db "whoami", 0; @ 21fe
L_.rodata_0x2205:
db "Richard Mlynarik", 0; @ 2205
L_.rodata_0x2216:
db "1.0", 0; @ 2216
L_.rodata_0x221a:
db "extra operand %s", 0; @ 221a
db 00h
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x2230:
db "cannot find name for user ID %ju", 0; @ 2230
L_.rodata_0x2251:
db "help", 0; @ 2251
L_.rodata_0x2256:
db "version", 0; @ 2256
L_.rodata_END:

section .init_array align=8 ; @3d20
L_.init_array_0x3d20:
L_reloc_0x3d20_0x13a0:
dq frame_dummy    ; 0x13a0 --> frame_dummy
L_.init_array_END:

section .fini_array align=8 ; @3d28
L_.fini_array_0x3d28:
L_reloc_0x3d28_0x1360:
dq __do_global_dtors_aux    ; 0x1360 --> __do_global_dtors_aux
L_.fini_array_END:

section .got align=8 ; @3f20
L_.got_0x3f20:
db "0=", 0; @ 3f20
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
dq __errno_location    ; 
dq strcpy    ; 
dq puts    ; 
dq fclose    ; 
dq getpwuid    ; 
dq strlen    ; 
dq __stack_chk_fail    ; 
dq getopt_long    ; 
dq printf    ; 
dq strrchr    ; 
dq geteuid    ; 
dq fputc    ; 
dq fprintf    ; 
dq malloc    ; 
dq setlocale    ; 
dq vfprintf    ; 
dq __cxa_atexit    ; 
dq exit    ; 
dq fwrite    ; 
dq strerror    ; 
dq __libc_start_main    ; 
dq _ITM_deregisterTMCloneTable    ; 
dq __gmon_start__    ; 
dq _ITM_registerTMCloneTable    ; 
dq __cxa_finalize    ; 
L_.got_END:




section .data align=32 ; @4000
__data_start:
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
__dso_handle:
dq __dso_handle    ; 0x4008 --> __dso_handle
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
L_reloc_0x4020_0x2251:
dq L_.rodata_0x2251    ; 0x2251 --> L_.rodata_0x2251
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db "h", 0; @ 4038
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
L_reloc_0x4040_0x2256:
dq L_.rodata_0x2256    ; 0x2256 --> L_.rodata_0x2256
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db "v", 0; @ 4058
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
L_.data_END:




section .bss align=32 ; @4080
L_.bss_0x4080:
resb 8
resb 24
resb 8
L_.bss_0x40a8:
resb 8
L_.bss_0x40b0:
resb 8
L_.bss_END:









section .bss
Ltemp_storage_foxdec:
resb 8
