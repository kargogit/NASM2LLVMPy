extern _ITM_deregisterTMCloneTable
extern _ITM_registerTMCloneTable
extern __ctype_b_loc
extern __cxa_finalize
extern __gmon_start__
extern __libc_start_main
extern exit
extern fclose
extern fgetc
extern fopen
extern fprintf
extern printf
extern putchar
extern puts
extern stderr
extern stdin
extern strcmp


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
global main
global print_bytes
global print_chars
global print_counts
global print_help
global print_lines
global print_max_line_length
global print_words
global process_file
global total_bytes
global total_chars
global total_lines
global total_max_line_length
global total_words


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
; Entry 1180; block 0; address 1180
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
  LEA RDI, [main]    ; 0x15d1 --> main
  CALL __libc_start_main wrt ..plt

; Entry 1180; block 1; address 11a5
L1180_1:
  HLT




; ------------------------------
; Function: deregister_tm_clones
; ------------------------------
; Entry 11b0; block 0; address 11b0
deregister_tm_clones:
  LEA RDI, [__TMC_END__]    ; 0x4010 --> __TMC_END__
  LEA RAX, [__TMC_END__]    ; 0x4010 --> __TMC_END__
  CMP RAX, RDI
  JZ L11b0_2    ; 0x11d8 --> L11b0_2

; Entry 11b0; block 1; address 11c3
L11b0_1:
  MOV qword [Ltemp_storage_foxdec], RBX ; inserted
  LEA RBX, [_ITM_deregisterTMCloneTable wrt ..plt]
  MOV RAX, RBX
  MOV RBX, qword [Ltemp_storage_foxdec] ; inserted
  TEST RAX, RAX
  JZ L11b0_2    ; 0x11d8 --> L11b0_2

; Entry 11b0; block 3; address 11cf
L11b0_3:
  ; Resolved indirection: RAX --> _ITM_deregisterTMCloneTable
  JMP _ITM_deregisterTMCloneTable wrt ..plt

; Entry 11b0; block 2; address 11d8
L11b0_2:
  RET




; -------------------------------
; Function: __do_global_dtors_aux
; -------------------------------
; Entry 1220; block 0; address 1220
__do_global_dtors_aux:
  CMP byte [L_.bss_0x4048], 0x0    ; 0x4048 --> L_.bss_0x4048
  JNZ L1220_2    ; 0x1258 --> L1220_2

; Entry 1220; block 1; address 122d
L1220_1:
  PUSH RBP
  MOV qword [Ltemp_storage_foxdec], RAX ; inserted
  LEA RAX, [__cxa_finalize wrt ..plt]
  CMP RAX, 0x0
  MOV RAX, qword [Ltemp_storage_foxdec] ; inserted
  MOV RBP, RSP
  JZ L1220_4    ; 0x1247 --> L1220_4

; Entry 1220; block 3; address 123b
L1220_3:
  MOV RDI, qword [__dso_handle]    ; 0x4008 --> __dso_handle
  CALL __cxa_finalize wrt ..plt

; Entry 1220; block 4; address 1247
L1220_4:
  CALL deregister_tm_clones    ; 0x11b0 --> deregister_tm_clones

; Entry 1220; block 5; address 124c
L1220_5:
  MOV byte [L_.bss_0x4048], 0x1    ; 0x4048 --> L_.bss_0x4048
  POP RBP
  RET

; Entry 1220; block 2; address 1258
L1220_2:
  RET




; ---------------------
; Function: frame_dummy
; ---------------------
; Entry 1260; block 1; address 1204
L1260_1:
  MOV qword [Ltemp_storage_foxdec], RBX ; inserted
  LEA RBX, [_ITM_registerTMCloneTable wrt ..plt]
  MOV RAX, RBX
  MOV RBX, qword [Ltemp_storage_foxdec] ; inserted
  TEST RAX, RAX
  JZ L1260_2    ; 0x1218 --> L1260_2

; Entry 1260; block 3; address 1210
L1260_3:
  ; Resolved indirection: RAX --> _ITM_registerTMCloneTable
  JMP _ITM_registerTMCloneTable wrt ..plt

; Entry 1260; block 2; address 1218
L1260_2:
  RET

; Entry 1260; block 0; address 1260
frame_dummy:
  LEA RDI, [__TMC_END__]    ; 0x4010 --> __TMC_END__
  LEA RSI, [__TMC_END__]    ; 0x4010 --> __TMC_END__
  SUB RSI, RDI
  MOV RAX, RSI
  SHR RSI, 0x3f
  SAR RAX, 0x3
  ADD RSI, RAX
  SAR RSI, 0x1
  JZ L1260_2    ; 0x1218 --> L1260_2
  JMP L1260_1 ; jump is inserted




; ----------------------
; Function: print_counts
; ----------------------
; Entry 1269; block 0; address 1269
print_counts:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x30
  MOV qword [RBP - 0x8], RDI
  MOV qword [RBP - 0x10], RSI
  MOV qword [RBP - 0x18], RDX
  MOV qword [RBP - 0x20], RCX
  MOV qword [RBP - 0x28], R8
  MOV qword [RBP - 0x30], R9
  MOV EAX, dword [L_.bss_0x4050]    ; 0x4050 --> L_.bss_0x4050
  TEST EAX, EAX
  JZ L1269_2    ; 0x12b2 --> L1269_2

; Entry 1269; block 1; address 1297
L1269_1:
  MOV RAX, qword [RBP - 0x8]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2008]    ; 0x2008 --> L_.rodata_0x2008
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1269; block 2; address 12b2
L1269_2:
  MOV EAX, dword [L_.bss_0x4054]    ; 0x4054 --> L_.bss_0x4054
  TEST EAX, EAX
  JZ L1269_4    ; 0x12d7 --> L1269_4

; Entry 1269; block 3; address 12bc
L1269_3:
  MOV RAX, qword [RBP - 0x10]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2008]    ; 0x2008 --> L_.rodata_0x2008
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1269; block 4; address 12d7
L1269_4:
  MOV EAX, dword [L_.bss_0x4058]    ; 0x4058 --> L_.bss_0x4058
  TEST EAX, EAX
  JZ L1269_6    ; 0x12fc --> L1269_6

; Entry 1269; block 5; address 12e1
L1269_5:
  MOV RAX, qword [RBP - 0x18]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2008]    ; 0x2008 --> L_.rodata_0x2008
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1269; block 6; address 12fc
L1269_6:
  MOV EAX, dword [L_.bss_0x405c]    ; 0x405c --> L_.bss_0x405c
  TEST EAX, EAX
  JZ L1269_8    ; 0x1321 --> L1269_8

; Entry 1269; block 7; address 1306
L1269_7:
  MOV RAX, qword [RBP - 0x20]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2008]    ; 0x2008 --> L_.rodata_0x2008
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1269; block 8; address 1321
L1269_8:
  MOV EAX, dword [L_.bss_0x4060]    ; 0x4060 --> L_.bss_0x4060
  TEST EAX, EAX
  JZ L1269_10    ; 0x1346 --> L1269_10

; Entry 1269; block 9; address 132b
L1269_9:
  MOV RAX, qword [RBP - 0x28]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2008]    ; 0x2008 --> L_.rodata_0x2008
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1269; block 10; address 1346
L1269_10:
  CMP qword [RBP - 0x30], 0x0
  JZ L1269_12    ; 0x135b --> L1269_12

; Entry 1269; block 11; address 134d
L1269_11:
  MOV RAX, qword [RBP - 0x30]
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 1269; block 13; address 1359
L1269_13:
  JMP L1269_14    ; 0x1365 --> L1269_14

; Entry 1269; block 12; address 135b
L1269_12:
  MOV EDI, 0xa
  CALL putchar wrt ..plt

; Entry 1269; block 14; address 1365
L1269_14:
  LEAVE
  RET




; ----------------------
; Function: process_file
; ----------------------
; Entry 1368; block 0; address 1368
process_file:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x50
  MOV qword [RBP - 0x48], RDI
  MOV qword [RBP - 0x50], RSI
  MOV qword [RBP - 0x30], 0x0
  MOV qword [RBP - 0x28], 0x0
  MOV qword [RBP - 0x20], 0x0
  MOV qword [RBP - 0x18], 0x0
  MOV qword [RBP - 0x10], 0x0
  MOV qword [RBP - 0x8], 0x0
  MOV dword [RBP - 0x38], 0x0
  JMP L1368_6    ; 0x1430 --> L1368_6

; Entry 1368; block 11; address 13b5
L1368_11:
  ADD qword [RBP - 0x18], 0x1
  ADD qword [RBP - 0x20], 0x1
  CMP dword [RBP - 0x34], 0xa
  JNZ L1368_3    ; 0x13ed --> L1368_3

; Entry 1368; block 2; address 13c5
L1368_2:
  ADD qword [RBP - 0x30], 0x1
  MOV RAX, qword [RBP - 0x8]
  CMP qword [RBP - 0x10], RAX
  JAE L1368_5    ; 0x13dc --> L1368_5

; Entry 1368; block 4; address 13d4
L1368_4:
  MOV RAX, qword [RBP - 0x8]
  MOV qword [RBP - 0x10], RAX

; Entry 1368; block 5; address 13dc
L1368_5:
  MOV qword [RBP - 0x8], 0x0
  MOV dword [RBP - 0x38], 0x0
  JMP L1368_6    ; 0x1430 --> L1368_6

; Entry 1368; block 3; address 13ed
L1368_3:
  ADD qword [RBP - 0x8], 0x1
  CALL __ctype_b_loc wrt ..plt

; Entry 1368; block 7; address 13f7
L1368_7:
  MOV RAX, qword [RAX]
  MOV EDX, dword [RBP - 0x34]
  MOVSXD RDX, EDX
  ADD RDX, RDX
  ADD RAX, RDX
  MOVZX EAX, word [RAX]
  MOVZX EAX, AX
  AND EAX, 0x2000
  TEST EAX, EAX
  JZ L1368_9    ; 0x141e --> L1368_9

; Entry 1368; block 8; address 1415
L1368_8:
  MOV dword [RBP - 0x38], 0x0
  JMP L1368_6    ; 0x1430 --> L1368_6

; Entry 1368; block 9; address 141e
L1368_9:
  CMP dword [RBP - 0x38], 0x0
  JNZ L1368_6    ; 0x1430 --> L1368_6

; Entry 1368; block 10; address 1424
L1368_10:
  ADD qword [RBP - 0x28], 0x1
  MOV dword [RBP - 0x38], 0x1

; Entry 1368; block 6; address 1430
L1368_6:
  MOV RAX, qword [RBP - 0x48]
  MOV RDI, RAX
  CALL fgetc wrt ..plt

; Entry 1368; block 1; address 143c
L1368_1:
  MOV dword [RBP - 0x34], EAX
  CMP dword [RBP - 0x34], 0xffffffff
  JNZ L1368_11    ; 0x13b5 --> L1368_11

; Entry 1368; block 12; address 1449
L1368_12:
  CMP qword [RBP - 0x8], 0x0
  JZ L1368_14    ; 0x1467 --> L1368_14

; Entry 1368; block 13; address 1450
L1368_13:
  ADD qword [RBP - 0x30], 0x1
  MOV RAX, qword [RBP - 0x8]
  CMP qword [RBP - 0x10], RAX
  JAE L1368_14    ; 0x1467 --> L1368_14

; Entry 1368; block 15; address 145f
L1368_15:
  MOV RAX, qword [RBP - 0x8]
  MOV qword [RBP - 0x10], RAX

; Entry 1368; block 14; address 1467
L1368_14:
  MOV RDX, qword [L_.bss_0x4068]    ; 0x4068 --> L_.bss_0x4068
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV qword [L_.bss_0x4068], RAX    ; 0x4068 --> L_.bss_0x4068
  MOV RDX, qword [L_.bss_0x4070]    ; 0x4070 --> L_.bss_0x4070
  MOV RAX, qword [RBP - 0x28]
  ADD RAX, RDX
  MOV qword [L_.bss_0x4070], RAX    ; 0x4070 --> L_.bss_0x4070
  MOV RDX, qword [L_.bss_0x4078]    ; 0x4078 --> L_.bss_0x4078
  MOV RAX, qword [RBP - 0x20]
  ADD RAX, RDX
  MOV qword [L_.bss_0x4078], RAX    ; 0x4078 --> L_.bss_0x4078
  MOV RDX, qword [L_.bss_0x4080]    ; 0x4080 --> L_.bss_0x4080
  MOV RAX, qword [RBP - 0x18]
  ADD RAX, RDX
  MOV qword [L_.bss_0x4080], RAX    ; 0x4080 --> L_.bss_0x4080
  MOV RAX, qword [L_.bss_0x4088]    ; 0x4088 --> L_.bss_0x4088
  CMP RAX, qword [RBP - 0x10]
  JAE L1368_17    ; 0x14d3 --> L1368_17

; Entry 1368; block 16; address 14c8
L1368_16:
  MOV RAX, qword [RBP - 0x10]
  MOV qword [L_.bss_0x4088], RAX    ; 0x4088 --> L_.bss_0x4088

; Entry 1368; block 17; address 14d3
L1368_17:
  MOV R8, qword [RBP - 0x50]
  MOV RDI, qword [RBP - 0x10]
  MOV RCX, qword [RBP - 0x18]
  MOV RDX, qword [RBP - 0x20]
  MOV RSI, qword [RBP - 0x28]
  MOV RAX, qword [RBP - 0x30]
  MOV R9, R8
  MOV R8, RDI
  MOV RDI, RAX
  CALL print_counts    ; 0x1269 --> print_counts

; Entry 1368; block 18; address 14f9
L1368_18:
  LEAVE
  RET




; --------------------
; Function: print_help
; --------------------
; Entry 14fc; block 0; address 14fc
print_help:
  PUSH RBP
  MOV RBP, RSP
  LEA RAX, [L_.rodata_0x2010]    ; 0x2010 --> L_.rodata_0x2010
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 1; address 1513
L14fc_1:
  LEA RAX, [L_.rodata_0x2030]    ; 0x2030 --> L_.rodata_0x2030
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 2; address 1522
L14fc_2:
  LEA RAX, [L_.rodata_0x2078]    ; 0x2078 --> L_.rodata_0x2078
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 3; address 1531
L14fc_3:
  LEA RAX, [L_.rodata_0x20c8]    ; 0x20c8 --> L_.rodata_0x20c8
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 4; address 1540
L14fc_4:
  LEA RAX, [L_.rodata_0x2110]    ; 0x2110 --> L_.rodata_0x2110
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 5; address 154f
L14fc_5:
  LEA RAX, [L_.rodata_0x2148]    ; 0x2148 --> L_.rodata_0x2148
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 6; address 155e
L14fc_6:
  LEA RAX, [L_.rodata_0x2198]    ; 0x2198 --> L_.rodata_0x2198
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 7; address 156d
L14fc_7:
  LEA RAX, [L_.rodata_0x21e8]    ; 0x21e8 --> L_.rodata_0x21e8
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 8; address 157c
L14fc_8:
  LEA RAX, [L_.rodata_0x2210]    ; 0x2210 --> L_.rodata_0x2210
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 9; address 158b
L14fc_9:
  LEA RAX, [L_.rodata_0x2240]    ; 0x2240 --> L_.rodata_0x2240
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 10; address 159a
L14fc_10:
  LEA RAX, [L_.rodata_0x2270]    ; 0x2270 --> L_.rodata_0x2270
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 11; address 15a9
L14fc_11:
  LEA RAX, [L_.rodata_0x22a0]    ; 0x22a0 --> L_.rodata_0x22a0
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 12; address 15b8
L14fc_12:
  LEA RAX, [L_.rodata_0x22c8]    ; 0x22c8 --> L_.rodata_0x22c8
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 14fc; block 13; address 15c7
L14fc_13:
  MOV EDI, 0x0
  NOP
FOXDEC_TERMINATING_L14fc_13:
  CALL exit wrt ..plt




; --------------
; Function: main
; --------------
; Entry 15d1; block 0; address 15d1
main:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x30
  MOV dword [RBP - 0x24], EDI
  MOV qword [RBP - 0x30], RSI
  MOV dword [RBP - 0x18], 0x1
  JMP L15d1_24    ; 0x173b --> L15d1_24

; Entry 15d1; block 25; address 15f0
L15d1_25:
  MOV EAX, dword [RBP - 0x18]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  LEA RDX, [L_.rodata_0x22f3]    ; 0x22f3 --> L_.rodata_0x22f3
  MOV RSI, RDX
  MOV RDI, RAX
  CALL strcmp wrt ..plt

; Entry 15d1; block 3; address 1619
L15d1_3:
  TEST EAX, EAX
  JNZ L15d1_5    ; 0x1627 --> L15d1_5

; Entry 15d1; block 4; address 161d
L15d1_4:
  NOP
FOXDEC_TERMINATING_L15d1_4:
  CALL print_help    ; 0x14fc --> print_help
L15d1_4_HLT:
  HLT ; should never be reached    ; 0x1622 --> L15d1_4_HLT

; Entry 15d1; block 5; address 1627
L15d1_5:
  MOV dword [RBP - 0x14], 0x1
  JMP L15d1_21    ; 0x170d --> L15d1_21

; Entry 15d1; block 22; address 1633
L15d1_22:
  MOV EAX, dword [RBP - 0x18]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RDX, qword [RAX]
  MOV EAX, dword [RBP - 0x14]
  CDQE
  ADD RAX, RDX
  MOVZX EAX, byte [RAX]
  MOVSX EAX, AL
  CMP EAX, 0x77
  JZ L15d1_7    ; 0x16a4 --> L15d1_7

; Entry 15d1; block 6; address 165d
L15d1_6:
  CMP EAX, 0x77
  JG L15d1_9    ; 0x16bc --> L15d1_9

; Entry 15d1; block 8; address 1662
L15d1_8:
  CMP EAX, 0x6d
  JZ L15d1_11    ; 0x168c --> L15d1_11

; Entry 15d1; block 10; address 1667
L15d1_10:
  CMP EAX, 0x6d
  JG L15d1_9    ; 0x16bc --> L15d1_9

; Entry 15d1; block 12; address 166c
L15d1_12:
  CMP EAX, 0x6c
  JZ L15d1_14    ; 0x1698 --> L15d1_14

; Entry 15d1; block 13; address 1671
L15d1_13:
  CMP EAX, 0x6c
  JG L15d1_9    ; 0x16bc --> L15d1_9

; Entry 15d1; block 15; address 1676
L15d1_15:
  CMP EAX, 0x4c
  JZ L15d1_17    ; 0x16b0 --> L15d1_17

; Entry 15d1; block 16; address 167b
L15d1_16:
  CMP EAX, 0x63
  JNZ L15d1_9    ; 0x16bc --> L15d1_9

; Entry 15d1; block 18; address 1680
L15d1_18:
  MOV dword [L_.bss_0x405c], 0x1    ; 0x405c --> L_.bss_0x405c
  JMP L15d1_19    ; 0x1709 --> L15d1_19

; Entry 15d1; block 11; address 168c
L15d1_11:
  MOV dword [L_.bss_0x4058], 0x1    ; 0x4058 --> L_.bss_0x4058
  JMP L15d1_19    ; 0x1709 --> L15d1_19

; Entry 15d1; block 14; address 1698
L15d1_14:
  MOV dword [L_.bss_0x4050], 0x1    ; 0x4050 --> L_.bss_0x4050
  JMP L15d1_19    ; 0x1709 --> L15d1_19

; Entry 15d1; block 7; address 16a4
L15d1_7:
  MOV dword [L_.bss_0x4054], 0x1    ; 0x4054 --> L_.bss_0x4054
  JMP L15d1_19    ; 0x1709 --> L15d1_19

; Entry 15d1; block 17; address 16b0
L15d1_17:
  MOV dword [L_.bss_0x4060], 0x1    ; 0x4060 --> L_.bss_0x4060
  JMP L15d1_19    ; 0x1709 --> L15d1_19

; Entry 15d1; block 9; address 16bc
L15d1_9:
  MOV EAX, dword [RBP - 0x18]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RDX, qword [RAX]
  MOV EAX, dword [RBP - 0x14]
  CDQE
  ADD RAX, RDX
  MOVZX EAX, byte [RAX]
  MOVSX EDX, AL
  MOV RAX, qword [stderr]    ; 0x4040 --> stderr
  LEA RCX, [L_.rodata_0x22fa]    ; 0x22fa --> L_.rodata_0x22fa
  MOV RSI, RCX
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL fprintf wrt ..plt

; Entry 15d1; block 20; address 16ff
L15d1_20:
  MOV EDI, 0x1
  NOP
FOXDEC_TERMINATING_L15d1_20:
  CALL exit wrt ..plt

; Entry 15d1; block 19; address 1709
L15d1_19:
  ADD dword [RBP - 0x14], 0x1

; Entry 15d1; block 21; address 170d
L15d1_21:
  MOV EAX, dword [RBP - 0x18]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RDX, qword [RAX]
  MOV EAX, dword [RBP - 0x14]
  CDQE
  ADD RAX, RDX
  MOVZX EAX, byte [RAX]
  TEST AL, AL
  JNZ L15d1_22    ; 0x1633 --> L15d1_22

; Entry 15d1; block 23; address 1737
L15d1_23:
  ADD dword [RBP - 0x18], 0x1

; Entry 15d1; block 24; address 173b
L15d1_24:
  MOV EAX, dword [RBP - 0x18]
  CMP EAX, dword [RBP - 0x24]
  JGE L15d1_2    ; 0x1765 --> L15d1_2

; Entry 15d1; block 1; address 1743
L15d1_1:
  MOV EAX, dword [RBP - 0x18]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  MOVZX EAX, byte [RAX]
  CMP AL, 0x2d
  JZ L15d1_25    ; 0x15f0 --> L15d1_25

; Entry 15d1; block 2; address 1765
L15d1_2:
  MOV EAX, dword [L_.bss_0x4050]    ; 0x4050 --> L_.bss_0x4050
  TEST EAX, EAX
  JNZ L15d1_27    ; 0x17b5 --> L15d1_27

; Entry 15d1; block 26; address 176f
L15d1_26:
  MOV EAX, dword [L_.bss_0x4054]    ; 0x4054 --> L_.bss_0x4054
  TEST EAX, EAX
  JNZ L15d1_27    ; 0x17b5 --> L15d1_27

; Entry 15d1; block 28; address 1779
L15d1_28:
  MOV EAX, dword [L_.bss_0x4058]    ; 0x4058 --> L_.bss_0x4058
  TEST EAX, EAX
  JNZ L15d1_27    ; 0x17b5 --> L15d1_27

; Entry 15d1; block 29; address 1783
L15d1_29:
  MOV EAX, dword [L_.bss_0x405c]    ; 0x405c --> L_.bss_0x405c
  TEST EAX, EAX
  JNZ L15d1_27    ; 0x17b5 --> L15d1_27

; Entry 15d1; block 30; address 178d
L15d1_30:
  MOV EAX, dword [L_.bss_0x4060]    ; 0x4060 --> L_.bss_0x4060
  TEST EAX, EAX
  JNZ L15d1_27    ; 0x17b5 --> L15d1_27

; Entry 15d1; block 31; address 1797
L15d1_31:
  MOV dword [L_.bss_0x4050], 0x1    ; 0x4050 --> L_.bss_0x4050
  MOV dword [L_.bss_0x4054], 0x1    ; 0x4054 --> L_.bss_0x4054
  MOV dword [L_.bss_0x405c], 0x1    ; 0x405c --> L_.bss_0x405c

; Entry 15d1; block 27; address 17b5
L15d1_27:
  MOV EAX, dword [RBP - 0x24]
  SUB EAX, dword [RBP - 0x18]
  MOV dword [RBP - 0xc], EAX
  CMP dword [RBP - 0xc], 0x0
  JNZ L15d1_33    ; 0x17dd --> L15d1_33

; Entry 15d1; block 32; address 17c4
L15d1_32:
  MOV RAX, qword [stdin]    ; 0x4020 --> stdin
  MOV ESI, 0x0
  MOV RDI, RAX
  CALL process_file    ; 0x1368 --> process_file

; Entry 15d1; block 34; address 17d8
L15d1_34:
  JMP L15d1_47    ; 0x18e0 --> L15d1_47

; Entry 15d1; block 33; address 17dd
L15d1_33:
  MOV EAX, dword [RBP - 0x18]
  MOV dword [RBP - 0x10], EAX
  JMP L15d1_45    ; 0x18d4 --> L15d1_45

; Entry 15d1; block 46; address 17e8
L15d1_46:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  LEA RDX, [L_.rodata_0x230e]    ; 0x230e --> L_.rodata_0x230e
  MOV RSI, RDX
  MOV RDI, RAX
  CALL strcmp wrt ..plt

; Entry 15d1; block 35; address 1811
L15d1_35:
  TEST EAX, EAX
  JNZ L15d1_37    ; 0x1833 --> L15d1_37

; Entry 15d1; block 36; address 1815
L15d1_36:
  MOV RAX, qword [stdin]    ; 0x4020 --> stdin
  LEA RDX, [L_.rodata_0x2310]    ; 0x2310 --> L_.rodata_0x2310
  MOV RSI, RDX
  MOV RDI, RAX
  CALL process_file    ; 0x1368 --> process_file

; Entry 15d1; block 38; address 182e
L15d1_38:
  JMP L15d1_43    ; 0x18d0 --> L15d1_43

; Entry 15d1; block 37; address 1833
L15d1_37:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  LEA RDX, [L_.rodata_0x231f]    ; 0x231f --> L_.rodata_0x231f
  MOV RSI, RDX
  MOV RDI, RAX
  CALL fopen wrt ..plt

; Entry 15d1; block 39; address 185c
L15d1_39:
  MOV qword [RBP - 0x8], RAX
  CMP qword [RBP - 0x8], 0x0
  JNZ L15d1_41    ; 0x189e --> L15d1_41

; Entry 15d1; block 40; address 1867
L15d1_40:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RDX, qword [RAX]
  MOV RAX, qword [stderr]    ; 0x4040 --> stderr
  LEA RCX, [L_.rodata_0x2321]    ; 0x2321 --> L_.rodata_0x2321
  MOV RSI, RCX
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL fprintf wrt ..plt

; Entry 15d1; block 42; address 189c
L15d1_42:
  JMP L15d1_43    ; 0x18d0 --> L15d1_43

; Entry 15d1; block 41; address 189e
L15d1_41:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RDX, qword [RAX]
  MOV RAX, qword [RBP - 0x8]
  MOV RSI, RDX
  MOV RDI, RAX
  CALL process_file    ; 0x1368 --> process_file

; Entry 15d1; block 44; address 18c4
L15d1_44:
  MOV RAX, qword [RBP - 0x8]
  MOV RDI, RAX
  CALL fclose wrt ..plt

; Entry 15d1; block 43; address 18d0
L15d1_43:
  ADD dword [RBP - 0x10], 0x1

; Entry 15d1; block 45; address 18d4
L15d1_45:
  MOV EAX, dword [RBP - 0x10]
  CMP EAX, dword [RBP - 0x24]
  JL L15d1_46    ; 0x17e8 --> L15d1_46

; Entry 15d1; block 47; address 18e0
L15d1_47:
  CMP dword [RBP - 0xc], 0x1
  JLE L15d1_49    ; 0x191b --> L15d1_49

; Entry 15d1; block 48; address 18e6
L15d1_48:
  MOV RDI, qword [L_.bss_0x4088]    ; 0x4088 --> L_.bss_0x4088
  MOV RCX, qword [L_.bss_0x4080]    ; 0x4080 --> L_.bss_0x4080
  MOV RDX, qword [L_.bss_0x4078]    ; 0x4078 --> L_.bss_0x4078
  MOV RSI, qword [L_.bss_0x4070]    ; 0x4070 --> L_.bss_0x4070
  MOV RAX, qword [L_.bss_0x4068]    ; 0x4068 --> L_.bss_0x4068
  LEA R9, [L_.rodata_0x2336]    ; 0x2336 --> L_.rodata_0x2336
  MOV R8, RDI
  MOV RDI, RAX
  CALL print_counts    ; 0x1269 --> print_counts

; Entry 15d1; block 49; address 191b
L15d1_49:
  MOV EAX, 0x0
  LEAVE
  RET




; ---------------
; Function: _fini
; ---------------
; Entry 1924; block 0; address 1924
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
db "%llu ", 0; @ 2008
db 00h
db 00h
L_.rodata_0x2010:
db "Usage: wc [OPTION]... [FILE]...", 0; @ 2010
L_.rodata_0x2030:
db "Print newline, word, and byte counts for each FILE, and a total line if", 0; @ 2030
L_.rodata_0x2078:
db "more than one FILE is specified.  A word is a nonempty sequence of non white", 0; @ 2078
db 00h
db 00h
db 00h
L_.rodata_0x20c8:
db "space delimited by white space characters or by start or end of input.\n", 0; @ 20c8
L_.rodata_0x2110:
db "With no FILE, or when FILE is -, read standard input.\n", 0; @ 2110
db 00h
L_.rodata_0x2148:
db "The options below may be used to select which counts are printed, always in", 0; @ 2148
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x2198:
db "the following order: newline, word, character, byte, maximum line length.", 0; @ 2198
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x21e8:
db "  -c            print the byte counts", 0; @ 21e8
db 00h
db 00h
L_.rodata_0x2210:
db "  -m            print the character counts", 0; @ 2210
db 00h
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x2240:
db "  -l            print the newline counts", 0; @ 2240
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
db 00h
L_.rodata_0x2270:
db "  -L            print the maximum line length", 0; @ 2270
db 00h
db 00h
L_.rodata_0x22a0:
db "  -w            print the word counts", 0; @ 22a0
db 00h
db 00h
L_.rodata_0x22c8:
db "      --help    display this help and exit", 0; @ 22c8
L_.rodata_0x22f3:
db "--help", 0; @ 22f3
L_.rodata_0x22fa:
db "Invalid option -%c\n", 0; @ 22fa
L_.rodata_0x230e:
db "-", 0; @ 230e
L_.rodata_0x2310:
db "standard input", 0; @ 2310
L_.rodata_0x231f:
db "r", 0; @ 231f
L_.rodata_0x2321:
db "Cannot open file %s\n", 0; @ 2321
L_.rodata_0x2336:
db "total", 0; @ 2336
__GNU_EH_FRAME_HDR:

section .init_array align=8 ; @3d70
L_.init_array_0x3d70:
L_reloc_0x3d70_0x1260:
dq frame_dummy    ; 0x1260 --> frame_dummy
L_.init_array_END:

section .fini_array align=8 ; @3d78
L_.fini_array_0x3d78:
L_reloc_0x3d78_0x1220:
dq __do_global_dtors_aux    ; 0x1220 --> __do_global_dtors_aux
L_.fini_array_END:

section .got align=8 ; @3f70
L_.got_0x3f70:
db 080h
db "=", 0; @ 3f71
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
dq putchar    ; 
dq puts    ; 
dq fclose    ; 
dq printf    ; 
dq fgetc    ; 
dq strcmp    ; 
dq fprintf    ; 
dq fopen    ; 
dq exit    ; 
dq __ctype_b_loc    ; 
dq __libc_start_main    ; 
dq _ITM_deregisterTMCloneTable    ; 
dq __gmon_start__    ; 
dq _ITM_registerTMCloneTable    ; 
dq __cxa_finalize    ; 
L_.got_END:




section .data align=8 ; @4000
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
__TMC_END__:




section .bss align=32 ; @4020
L_.bss_0x4020:
resb 32
resb 8
L_.bss_0x4048:
resb 8
L_.bss_0x4050:
resb 4
L_.bss_0x4054:
resb 4
L_.bss_0x4058:
resb 4
L_.bss_0x405c:
resb 4
L_.bss_0x4060:
resb 8
L_.bss_0x4068:
resb 8
L_.bss_0x4070:
resb 8
L_.bss_0x4078:
resb 8
L_.bss_0x4080:
resb 8
L_.bss_0x4088:
resb 8
L_.bss_END:









section .bss
Ltemp_storage_foxdec:
resb 8
