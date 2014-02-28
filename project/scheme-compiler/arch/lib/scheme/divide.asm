/* divide.asm * Computes the division of variadic number of integers: R0 <- ARG[0] / ARG[1] /... */ DIVIDE:  PUSH(FP);  MOV(FP, SP);  PUSH(R1);  PUSH(R2);  PUSH(R3);  PUSH(R4);    MOV(R4,FPARG(1));      CMP(R4, IMM(0));  JUMP_EQ(L_ZERO_ARGS_DIV);  CALL(MAKE_ARGS_FRACTIONS);  CMP(R4, IMM(1));  JUMP_EQ(HAS_ONE_ARGS_DIV);    MOV(R1, INDD(FPARG(2),1));  MOV(R0, INDD(FPARG(2),2));  MOV(R2, IMM(3));  DECR(R4);    L_START_DIV:  CMP(R4, IMM(0));  JUMP_EQ(L_FINISH_DIV);  CMP(INDD(FPARG(R2),1), IMM(0));  JUMP_EQ(DIV_BY_ZERO);  MUL(R1,INDD(FPARG(R2),2));  MUL(R0,INDD(FPARG(R2),1));  INCR(R2);  DECR(R4);  JUMP(L_START_DIV);    L_FINISH_DIV:  MOV(R3,R1);  REM(R3,R0);  CMP(R3, IMM(0));  JUMP_EQ(MAKE_INTEGER_DIV);  PUSH(R0);  PUSH(R1);  CALL(MAKE_SOB_FRACTION);  DROP(2);  JUMP(L_END_DIV);    HAS_ONE_ARGS_DIV:  CMP(INDD(FPARG(2),1),IMM(0));  JUMP_EQ(DIV_BY_ZERO);  MOV(R0,INDD(FPARG(2),1));  MOV(R1,INDD(FPARG(2),2));  MOV(INDD(FPARG(2),1),R1);  MOV(INDD(FPARG(2),2),R0);  MOV(R3,R1);  REM(R3,R0);  CMP(R3, IMM(0));  JUMP_EQ(MAKE_INTEGER_DIV);  PUSH(INDD(FPARG(2),2));  PUSH(INDD(FPARG(2),1));  CALL(MAKE_SOB_FRACTION);  DROP(2);  L_END_DIV:  POP(R4);  POP(R3);  POP(R2);  POP(R1);  POP(FP);  RETURN;    MAKE_INTEGER_DIV:  DIV(R1,R0);  PUSH(R1);  CALL(MAKE_SOB_INTEGER);  DROP(1);  POP(R4);  POP(R3);  POP(R2);  POP(R1);  POP(FP);  RETURN;    DIV_BY_ZERO:  CALL(ERROR_DIVISION_BY_ZERO);  L_ZERO_ARGS_DIV:  CALL(ERROR_NOT_ENOUGH_ARGS);