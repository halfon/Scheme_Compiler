/* INT_TO_CHAR.asm * Takes a number and Returns in R0 the character corresponding to the Unicode scalar value of the number */ INT_TO_CHAR:  PUSH(FP);  MOV(FP, SP);    CMP(FPARG(1), IMM(1));  JUMP_LT(HAS_NO_ARGS_INT_TO_CHAR);  JUMP_GT(TOO_MANY_ARGS_INT_TO_CHAR);  CMP(IND(FPARG(2)),T_INTEGER);  JUMP_NE(NOT_VALID_ARG_INT_TO_CHAR);    PUSH(INDD(FPARG(2),1));  CALL(MAKE_SOB_CHAR);  DROP(1);    POP(FP);  RETURN;    NOT_VALID_ARG_INT_TO_CHAR:  CALL(ERROR_NOT_VALID_ARG);    HAS_NO_ARGS_INT_TO_CHAR:  CALL(ERROR_NOT_ENOUGH_ARGS);    TOO_MANY_ARGS_INT_TO_CHAR:  CALL(ERROR_TOO_MANY_ARGS);