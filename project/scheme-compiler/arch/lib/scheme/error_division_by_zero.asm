 ERROR_DIVISION_BY_ZERO:  PUSH(FP);  MOV(FP, SP);    PUSH(IMM('\n'));  CALL(PUTCHAR);  PUSH(IMM('e'));  CALL(PUTCHAR);  PUSH(IMM('r'));  CALL(PUTCHAR);  PUSH(IMM('r'));  CALL(PUTCHAR);  PUSH(IMM('o'));  CALL(PUTCHAR);  PUSH(IMM('r'));  CALL(PUTCHAR);  PUSH(IMM(':'));  CALL(PUTCHAR);  PUSH(IMM(' '));  CALL(PUTCHAR);  PUSH(IMM('d'));  CALL(PUTCHAR);  PUSH(IMM('i'));  CALL(PUTCHAR);  PUSH(IMM('v'));  CALL(PUTCHAR);  PUSH(IMM('i'));  CALL(PUTCHAR);  PUSH(IMM('s'));  CALL(PUTCHAR);  PUSH(IMM('i'));  CALL(PUTCHAR);  PUSH(IMM('o'));  CALL(PUTCHAR);  PUSH(IMM('n'));  CALL(PUTCHAR);  PUSH(IMM(' '));  CALL(PUTCHAR);  PUSH(IMM('b'));  CALL(PUTCHAR);  PUSH(IMM('y'));  CALL(PUTCHAR);  PUSH(IMM(' '));  CALL(PUTCHAR);  PUSH(IMM('z'));  CALL(PUTCHAR);  PUSH(IMM('e'));  CALL(PUTCHAR);  PUSH(IMM('r'));  CALL(PUTCHAR);  PUSH(IMM('o'));  CALL(PUTCHAR);  DROP(24);  CALL(NEWLINE);  HALT;