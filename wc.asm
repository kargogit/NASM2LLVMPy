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
; Entry 1160; block 0; address 1160
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
  LEA RDI, [main]    ; 0x14dc --> main
  CALL __libc_start_main wrt ..plt

; Entry 1160; block 1; address 1185
L1160_1:
  HLT




; ------------------------------
; Function: deregister_tm_clones
; ------------------------------
; Entry 1190; block 0; address 1190
deregister_tm_clones:
  LEA RDI, [__TMC_END__]    ; 0x4010 --> __TMC_END__
  LEA RAX, [__TMC_END__]    ; 0x4010 --> __TMC_END__
  CMP RAX, RDI
  JZ L1190_2    ; 0x11b8 --> L1190_2

; Entry 1190; block 1; address 11a3
L1190_1:
  MOV qword [Ltemp_storage_foxdec], RBX ; inserted
  LEA RBX, [_ITM_deregisterTMCloneTable wrt ..plt]
  MOV RAX, RBX
  MOV RBX, qword [Ltemp_storage_foxdec] ; inserted
  TEST RAX, RAX
  JZ L1190_2    ; 0x11b8 --> L1190_2

; Entry 1190; block 3; address 11af
L1190_3:
  ; Resolved indirection: RAX --> _ITM_deregisterTMCloneTable
  JMP _ITM_deregisterTMCloneTable wrt ..plt

; Entry 1190; block 2; address 11b8
L1190_2:
  RET




; -------------------------------
; Function: __do_global_dtors_aux
; -------------------------------
; Entry 1200; block 0; address 1200
__do_global_dtors_aux:
  CMP byte [L_.bss_0x4048], 0x0    ; 0x4048 --> L_.bss_0x4048
  JNZ L1200_2    ; 0x1238 --> L1200_2

; Entry 1200; block 1; address 120d
L1200_1:
  PUSH RBP
  MOV qword [Ltemp_storage_foxdec], RAX ; inserted
  LEA RAX, [__cxa_finalize wrt ..plt]
  CMP RAX, 0x0
  MOV RAX, qword [Ltemp_storage_foxdec] ; inserted
  MOV RBP, RSP
  JZ L1200_4    ; 0x1227 --> L1200_4

; Entry 1200; block 3; address 121b
L1200_3:
  MOV RDI, qword [__dso_handle]    ; 0x4008 --> __dso_handle
  CALL __cxa_finalize wrt ..plt

; Entry 1200; block 4; address 1227
L1200_4:
  CALL deregister_tm_clones    ; 0x1190 --> deregister_tm_clones

; Entry 1200; block 5; address 122c
L1200_5:
  MOV byte [L_.bss_0x4048], 0x1    ; 0x4048 --> L_.bss_0x4048
  POP RBP
  RET

; Entry 1200; block 2; address 1238
L1200_2:
  RET




; ---------------------
; Function: frame_dummy
; ---------------------
; Entry 1240; block 1; address 11e4
L1240_1:
  MOV qword [Ltemp_storage_foxdec], RBX ; inserted
  LEA RBX, [_ITM_registerTMCloneTable wrt ..plt]
  MOV RAX, RBX
  MOV RBX, qword [Ltemp_storage_foxdec] ; inserted
  TEST RAX, RAX
  JZ L1240_2    ; 0x11f8 --> L1240_2

; Entry 1240; block 3; address 11f0
L1240_3:
  ; Resolved indirection: RAX --> _ITM_registerTMCloneTable
  JMP _ITM_registerTMCloneTable wrt ..plt

; Entry 1240; block 2; address 11f8
L1240_2:
  RET

; Entry 1240; block 0; address 1240
frame_dummy:
  LEA RDI, [__TMC_END__]    ; 0x4010 --> __TMC_END__
  LEA RSI, [__TMC_END__]    ; 0x4010 --> __TMC_END__
  SUB RSI, RDI
  MOV RAX, RSI
  SHR RSI, 0x3f
  SAR RAX, 0x3
  ADD RSI, RAX
  SAR RSI, 0x1
  JZ L1240_2    ; 0x11f8 --> L1240_2
  JMP L1240_1 ; jump is inserted




; ----------------------
; Function: print_counts
; ----------------------
; Entry 1249; block 0; address 1249
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
  JZ L1249_2    ; 0x1292 --> L1249_2

; Entry 1249; block 1; address 1277
L1249_1:
  MOV RAX, qword [RBP - 0x8]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2004]    ; 0x2004 --> L_.rodata_0x2004
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1249; block 2; address 1292
L1249_2:
  MOV EAX, dword [L_.bss_0x4054]    ; 0x4054 --> L_.bss_0x4054
  TEST EAX, EAX
  JZ L1249_4    ; 0x12b7 --> L1249_4

; Entry 1249; block 3; address 129c
L1249_3:
  MOV RAX, qword [RBP - 0x10]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2004]    ; 0x2004 --> L_.rodata_0x2004
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1249; block 4; address 12b7
L1249_4:
  MOV EAX, dword [L_.bss_0x4058]    ; 0x4058 --> L_.bss_0x4058
  TEST EAX, EAX
  JZ L1249_6    ; 0x12dc --> L1249_6

; Entry 1249; block 5; address 12c1
L1249_5:
  MOV RAX, qword [RBP - 0x18]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2004]    ; 0x2004 --> L_.rodata_0x2004
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1249; block 6; address 12dc
L1249_6:
  MOV EAX, dword [L_.bss_0x405c]    ; 0x405c --> L_.bss_0x405c
  TEST EAX, EAX
  JZ L1249_8    ; 0x1301 --> L1249_8

; Entry 1249; block 7; address 12e6
L1249_7:
  MOV RAX, qword [RBP - 0x20]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2004]    ; 0x2004 --> L_.rodata_0x2004
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1249; block 8; address 1301
L1249_8:
  MOV EAX, dword [L_.bss_0x4060]    ; 0x4060 --> L_.bss_0x4060
  TEST EAX, EAX
  JZ L1249_10    ; 0x1326 --> L1249_10

; Entry 1249; block 9; address 130b
L1249_9:
  MOV RAX, qword [RBP - 0x28]
  MOV RSI, RAX
  LEA RAX, [L_.rodata_0x2004]    ; 0x2004 --> L_.rodata_0x2004
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL printf wrt ..plt

; Entry 1249; block 10; address 1326
L1249_10:
  CMP qword [RBP - 0x30], 0x0
  JZ L1249_12    ; 0x133b --> L1249_12

; Entry 1249; block 11; address 132d
L1249_11:
  MOV RAX, qword [RBP - 0x30]
  MOV RDI, RAX
  CALL puts wrt ..plt

; Entry 1249; block 13; address 1339
L1249_13:
  JMP L1249_14    ; 0x1345 --> L1249_14

; Entry 1249; block 12; address 133b
L1249_12:
  MOV EDI, 0xa
  CALL putchar wrt ..plt

; Entry 1249; block 14; address 1345
L1249_14:
  LEAVE
  RET




; ----------------------
; Function: process_file
; ----------------------
; Entry 1348; block 0; address 1348
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
  JMP L1348_6    ; 0x1410 --> L1348_6

; Entry 1348; block 11; address 1395
L1348_11:
  ADD qword [RBP - 0x18], 0x1
  ADD qword [RBP - 0x20], 0x1
  CMP dword [RBP - 0x34], 0xa
  JNZ L1348_3    ; 0x13cd --> L1348_3

; Entry 1348; block 2; address 13a5
L1348_2:
  ADD qword [RBP - 0x30], 0x1
  MOV RAX, qword [RBP - 0x8]
  CMP qword [RBP - 0x10], RAX
  JAE L1348_5    ; 0x13bc --> L1348_5

; Entry 1348; block 4; address 13b4
L1348_4:
  MOV RAX, qword [RBP - 0x8]
  MOV qword [RBP - 0x10], RAX

; Entry 1348; block 5; address 13bc
L1348_5:
  MOV qword [RBP - 0x8], 0x0
  MOV dword [RBP - 0x38], 0x0
  JMP L1348_6    ; 0x1410 --> L1348_6

; Entry 1348; block 3; address 13cd
L1348_3:
  ADD qword [RBP - 0x8], 0x1
  CALL __ctype_b_loc wrt ..plt

; Entry 1348; block 7; address 13d7
L1348_7:
  MOV RAX, qword [RAX]
  MOV EDX, dword [RBP - 0x34]
  MOVSXD RDX, EDX
  ADD RDX, RDX
  ADD RAX, RDX
  MOVZX EAX, word [RAX]
  MOVZX EAX, AX
  AND EAX, 0x2000
  TEST EAX, EAX
  JZ L1348_9    ; 0x13fe --> L1348_9

; Entry 1348; block 8; address 13f5
L1348_8:
  MOV dword [RBP - 0x38], 0x0
  JMP L1348_6    ; 0x1410 --> L1348_6

; Entry 1348; block 9; address 13fe
L1348_9:
  CMP dword [RBP - 0x38], 0x0
  JNZ L1348_6    ; 0x1410 --> L1348_6

; Entry 1348; block 10; address 1404
L1348_10:
  ADD qword [RBP - 0x28], 0x1
  MOV dword [RBP - 0x38], 0x1

; Entry 1348; block 6; address 1410
L1348_6:
  MOV RAX, qword [RBP - 0x48]
  MOV RDI, RAX
  CALL fgetc wrt ..plt

; Entry 1348; block 1; address 141c
L1348_1:
  MOV dword [RBP - 0x34], EAX
  CMP dword [RBP - 0x34], 0xffffffff
  JNZ L1348_11    ; 0x1395 --> L1348_11

; Entry 1348; block 12; address 1429
L1348_12:
  CMP qword [RBP - 0x8], 0x0
  JZ L1348_14    ; 0x1447 --> L1348_14

; Entry 1348; block 13; address 1430
L1348_13:
  ADD qword [RBP - 0x30], 0x1
  MOV RAX, qword [RBP - 0x8]
  CMP qword [RBP - 0x10], RAX
  JAE L1348_14    ; 0x1447 --> L1348_14

; Entry 1348; block 15; address 143f
L1348_15:
  MOV RAX, qword [RBP - 0x8]
  MOV qword [RBP - 0x10], RAX

; Entry 1348; block 14; address 1447
L1348_14:
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
  JAE L1348_17    ; 0x14b3 --> L1348_17

; Entry 1348; block 16; address 14a8
L1348_16:
  MOV RAX, qword [RBP - 0x10]
  MOV qword [L_.bss_0x4088], RAX    ; 0x4088 --> L_.bss_0x4088

; Entry 1348; block 17; address 14b3
L1348_17:
  MOV R8, qword [RBP - 0x50]
  MOV RDI, qword [RBP - 0x10]
  MOV RCX, qword [RBP - 0x18]
  MOV RDX, qword [RBP - 0x20]
  MOV RSI, qword [RBP - 0x28]
  MOV RAX, qword [RBP - 0x30]
  MOV R9, R8
  MOV R8, RDI
  MOV RDI, RAX
  CALL print_counts    ; 0x1249 --> print_counts

; Entry 1348; block 18; address 14d9
L1348_18:
  LEAVE
  RET




; --------------
; Function: main
; --------------
; Entry 14dc; block 0; address 14dc
main:
  PUSH RBP
  MOV RBP, RSP
  SUB RSP, 0x30
  MOV dword [RBP - 0x24], EDI
  MOV qword [RBP - 0x30], RSI
  MOV dword [RBP - 0x18], 0x1
  JMP L14dc_21    ; 0x1631 --> L14dc_21

; Entry 14dc; block 22; address 14fb
L14dc_22:
  MOV EAX, dword [RBP - 0x18]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  MOVZX EAX, byte [RAX]
  CMP AL, 0x2d
  JNZ L14dc_2    ; 0x163f --> L14dc_2

; Entry 14dc; block 1; address 151d
L14dc_1:
  MOV dword [RBP - 0x14], 0x1
  JMP L14dc_18    ; 0x1603 --> L14dc_18

; Entry 14dc; block 19; address 1529
L14dc_19:
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
  JZ L14dc_4    ; 0x159a --> L14dc_4

; Entry 14dc; block 3; address 1553
L14dc_3:
  CMP EAX, 0x77
  JG L14dc_6    ; 0x15b2 --> L14dc_6

; Entry 14dc; block 5; address 1558
L14dc_5:
  CMP EAX, 0x6d
  JZ L14dc_8    ; 0x1582 --> L14dc_8

; Entry 14dc; block 7; address 155d
L14dc_7:
  CMP EAX, 0x6d
  JG L14dc_6    ; 0x15b2 --> L14dc_6

; Entry 14dc; block 9; address 1562
L14dc_9:
  CMP EAX, 0x6c
  JZ L14dc_11    ; 0x158e --> L14dc_11

; Entry 14dc; block 10; address 1567
L14dc_10:
  CMP EAX, 0x6c
  JG L14dc_6    ; 0x15b2 --> L14dc_6

; Entry 14dc; block 12; address 156c
L14dc_12:
  CMP EAX, 0x4c
  JZ L14dc_14    ; 0x15a6 --> L14dc_14

; Entry 14dc; block 13; address 1571
L14dc_13:
  CMP EAX, 0x63
  JNZ L14dc_6    ; 0x15b2 --> L14dc_6

; Entry 14dc; block 15; address 1576
L14dc_15:
  MOV dword [L_.bss_0x405c], 0x1    ; 0x405c --> L_.bss_0x405c
  JMP L14dc_16    ; 0x15ff --> L14dc_16

; Entry 14dc; block 8; address 1582
L14dc_8:
  MOV dword [L_.bss_0x4058], 0x1    ; 0x4058 --> L_.bss_0x4058
  JMP L14dc_16    ; 0x15ff --> L14dc_16

; Entry 14dc; block 11; address 158e
L14dc_11:
  MOV dword [L_.bss_0x4050], 0x1    ; 0x4050 --> L_.bss_0x4050
  JMP L14dc_16    ; 0x15ff --> L14dc_16

; Entry 14dc; block 4; address 159a
L14dc_4:
  MOV dword [L_.bss_0x4054], 0x1    ; 0x4054 --> L_.bss_0x4054
  JMP L14dc_16    ; 0x15ff --> L14dc_16

; Entry 14dc; block 14; address 15a6
L14dc_14:
  MOV dword [L_.bss_0x4060], 0x1    ; 0x4060 --> L_.bss_0x4060
  JMP L14dc_16    ; 0x15ff --> L14dc_16

; Entry 14dc; block 6; address 15b2
L14dc_6:
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
  LEA RCX, [L_.rodata_0x200a]    ; 0x200a --> L_.rodata_0x200a
  MOV RSI, RCX
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL fprintf wrt ..plt

; Entry 14dc; block 17; address 15f5
L14dc_17:
  MOV EDI, 0x1
  NOP
FOXDEC_TERMINATING_L14dc_17:
  CALL exit wrt ..plt

; Entry 14dc; block 16; address 15ff
L14dc_16:
  ADD dword [RBP - 0x14], 0x1

; Entry 14dc; block 18; address 1603
L14dc_18:
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
  JNZ L14dc_19    ; 0x1529 --> L14dc_19

; Entry 14dc; block 20; address 162d
L14dc_20:
  ADD dword [RBP - 0x18], 0x1

; Entry 14dc; block 21; address 1631
L14dc_21:
  MOV EAX, dword [RBP - 0x18]
  CMP EAX, dword [RBP - 0x24]
  JL L14dc_22    ; 0x14fb --> L14dc_22

; Entry 14dc; block 23; address 163d
L14dc_23:
  JMP L14dc_24    ; 0x1640 --> L14dc_24

; Entry 14dc; block 2; address 163f
L14dc_2:
  NOP ; NOP inserted

; Entry 14dc; block 24; address 1640
L14dc_24:
  MOV EAX, dword [L_.bss_0x4050]    ; 0x4050 --> L_.bss_0x4050
  TEST EAX, EAX
  JNZ L14dc_26    ; 0x1690 --> L14dc_26

; Entry 14dc; block 25; address 164a
L14dc_25:
  MOV EAX, dword [L_.bss_0x4054]    ; 0x4054 --> L_.bss_0x4054
  TEST EAX, EAX
  JNZ L14dc_26    ; 0x1690 --> L14dc_26

; Entry 14dc; block 27; address 1654
L14dc_27:
  MOV EAX, dword [L_.bss_0x4058]    ; 0x4058 --> L_.bss_0x4058
  TEST EAX, EAX
  JNZ L14dc_26    ; 0x1690 --> L14dc_26

; Entry 14dc; block 28; address 165e
L14dc_28:
  MOV EAX, dword [L_.bss_0x405c]    ; 0x405c --> L_.bss_0x405c
  TEST EAX, EAX
  JNZ L14dc_26    ; 0x1690 --> L14dc_26

; Entry 14dc; block 29; address 1668
L14dc_29:
  MOV EAX, dword [L_.bss_0x4060]    ; 0x4060 --> L_.bss_0x4060
  TEST EAX, EAX
  JNZ L14dc_26    ; 0x1690 --> L14dc_26

; Entry 14dc; block 30; address 1672
L14dc_30:
  MOV dword [L_.bss_0x4050], 0x1    ; 0x4050 --> L_.bss_0x4050
  MOV dword [L_.bss_0x4054], 0x1    ; 0x4054 --> L_.bss_0x4054
  MOV dword [L_.bss_0x405c], 0x1    ; 0x405c --> L_.bss_0x405c

; Entry 14dc; block 26; address 1690
L14dc_26:
  MOV EAX, dword [RBP - 0x24]
  SUB EAX, dword [RBP - 0x18]
  MOV dword [RBP - 0xc], EAX
  CMP dword [RBP - 0xc], 0x0
  JNZ L14dc_32    ; 0x16b8 --> L14dc_32

; Entry 14dc; block 31; address 169f
L14dc_31:
  MOV RAX, qword [stdin]    ; 0x4020 --> stdin
  MOV ESI, 0x0
  MOV RDI, RAX
  CALL process_file    ; 0x1348 --> process_file

; Entry 14dc; block 33; address 16b3
L14dc_33:
  JMP L14dc_46    ; 0x17ce --> L14dc_46

; Entry 14dc; block 32; address 16b8
L14dc_32:
  MOV EAX, dword [RBP - 0x18]
  MOV dword [RBP - 0x10], EAX
  JMP L14dc_44    ; 0x17c2 --> L14dc_44

; Entry 14dc; block 45; address 16c3
L14dc_45:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  MOVZX EAX, byte [RAX]
  CMP AL, 0x2d
  JNZ L14dc_35    ; 0x1721 --> L14dc_35

; Entry 14dc; block 34; address 16e1
L14dc_34:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  ADD RAX, 0x1
  MOVZX EAX, byte [RAX]
  TEST AL, AL
  JNZ L14dc_35    ; 0x1721 --> L14dc_35

; Entry 14dc; block 36; address 1703
L14dc_36:
  MOV RAX, qword [stdin]    ; 0x4020 --> stdin
  LEA RDX, [L_.rodata_0x201e]    ; 0x201e --> L_.rodata_0x201e
  MOV RSI, RDX
  MOV RDI, RAX
  CALL process_file    ; 0x1348 --> process_file

; Entry 14dc; block 37; address 171c
L14dc_37:
  JMP L14dc_42    ; 0x17be --> L14dc_42

; Entry 14dc; block 35; address 1721
L14dc_35:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RAX, qword [RAX]
  LEA RDX, [L_.rodata_0x202d]    ; 0x202d --> L_.rodata_0x202d
  MOV RSI, RDX
  MOV RDI, RAX
  CALL fopen wrt ..plt

; Entry 14dc; block 38; address 174a
L14dc_38:
  MOV qword [RBP - 0x8], RAX
  CMP qword [RBP - 0x8], 0x0
  JNZ L14dc_40    ; 0x178c --> L14dc_40

; Entry 14dc; block 39; address 1755
L14dc_39:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RDX, qword [RAX]
  MOV RAX, qword [stderr]    ; 0x4040 --> stderr
  LEA RCX, [L_.rodata_0x202f]    ; 0x202f --> L_.rodata_0x202f
  MOV RSI, RCX
  MOV RDI, RAX
  MOV EAX, 0x0
  CALL fprintf wrt ..plt

; Entry 14dc; block 41; address 178a
L14dc_41:
  JMP L14dc_42    ; 0x17be --> L14dc_42

; Entry 14dc; block 40; address 178c
L14dc_40:
  MOV EAX, dword [RBP - 0x10]
  CDQE
  LEA RDX, [RAX * 8]
  MOV RAX, qword [RBP - 0x30]
  ADD RAX, RDX
  MOV RDX, qword [RAX]
  MOV RAX, qword [RBP - 0x8]
  MOV RSI, RDX
  MOV RDI, RAX
  CALL process_file    ; 0x1348 --> process_file

; Entry 14dc; block 43; address 17b2
L14dc_43:
  MOV RAX, qword [RBP - 0x8]
  MOV RDI, RAX
  CALL fclose wrt ..plt

; Entry 14dc; block 42; address 17be
L14dc_42:
  ADD dword [RBP - 0x10], 0x1

; Entry 14dc; block 44; address 17c2
L14dc_44:
  MOV EAX, dword [RBP - 0x10]
  CMP EAX, dword [RBP - 0x24]
  JL L14dc_45    ; 0x16c3 --> L14dc_45

; Entry 14dc; block 46; address 17ce
L14dc_46:
  CMP dword [RBP - 0xc], 0x1
  JLE L14dc_48    ; 0x1809 --> L14dc_48

; Entry 14dc; block 47; address 17d4
L14dc_47:
  MOV RDI, qword [L_.bss_0x4088]    ; 0x4088 --> L_.bss_0x4088
  MOV RCX, qword [L_.bss_0x4080]    ; 0x4080 --> L_.bss_0x4080
  MOV RDX, qword [L_.bss_0x4078]    ; 0x4078 --> L_.bss_0x4078
  MOV RSI, qword [L_.bss_0x4070]    ; 0x4070 --> L_.bss_0x4070
  MOV RAX, qword [L_.bss_0x4068]    ; 0x4068 --> L_.bss_0x4068
  LEA R9, [L_.rodata_0x2044]    ; 0x2044 --> L_.rodata_0x2044
  MOV R8, RDI
  MOV RDI, RAX
  CALL print_counts    ; 0x1249 --> print_counts

; Entry 14dc; block 48; address 1809
L14dc_48:
  MOV EAX, 0x0
  LEAVE
  RET




; ---------------
; Function: _fini
; ---------------
; Entry 1810; block 0; address 1810
_fini:
  SUB RSP, 0x8
  ADD RSP, 0x8
  RET




section .rodata align=4 ; @2000
L_.rodata_0x2000:
db 01h
db 00h
db 02h
db 00h
L_.rodata_0x2004:
db "%llu ", 0; @ 2004
L_.rodata_0x200a:
db "Invalid option -%c\n", 0; @ 200a
L_.rodata_0x201e:
db "standard input", 0; @ 201e
L_.rodata_0x202d:
db "r", 0; @ 202d
L_.rodata_0x202f:
db "Cannot open file %s\n", 0; @ 202f
L_.rodata_0x2044:
db "total", 0; @ 2044
L_.rodata_END:

section .init_array align=8 ; @3d78
L_.init_array_0x3d78:
L_reloc_0x3d78_0x1240:
dq frame_dummy    ; 0x1240 --> frame_dummy
L_.init_array_END:

section .fini_array align=8 ; @3d80
L_.fini_array_0x3d80:
L_reloc_0x3d80_0x1200:
dq __do_global_dtors_aux    ; 0x1200 --> __do_global_dtors_aux
L_.fini_array_END:

section .got align=8 ; @3f78
L_.got_0x3f78:
db 088h
db "=", 0; @ 3f79
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
