/* zero.asm * Returns true iff all the argument is equal to zero: R0 <- TRUE iff ARG[0] = 0 */ ZERO:  PUSH(FP);  MOV(FP, SP);    CMP(FPARG(1), IMM(0));  JUMP_EQ(HAS_NO_ARGS_ZERO);  CMP(FPARG(1), IMM(2));  JUMP_GE(TOO_MANY_ARGS_ZERO);  CMP(INDD(FPARG(2),1), IMM(0));  JUMP_EQ(CREATE_TRUE_ZERO);  JUMP(CREATE_FALSE_ZERO);    HAS_NO_ARGS_ZERO:  CALL(ERROR_NOT_ENOUGH_ARGS);    TOO_MANY_ARGS_ZERO:  CALL(ERROR_TOO_MANY_ARGS);    CREATE_TRUE_ZERO:  MOV(R0,TRUE_CONSTANT);  POP(FP);  RETURN;    CREATE_FALSE_ZERO:  MOV(R0,FALSE_CONSTANT);  POP(FP);  RETURN;