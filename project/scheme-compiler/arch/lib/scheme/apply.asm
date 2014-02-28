/* APPLY.asm * Takes a procedure, variadic number of objs and a list (or empty list=NIL), * and return in R0 the values of applying procedure to objs and the elements of list  * STARG(i) = STACK[SP-2-i] * FPARG(i) = STACK[FP-3-i] */ APPLY:  PUSH(FP);  MOV(FP, SP);  PUSH(R1);  PUSH(R2);  PUSH(R3);    CMP(FPARG(1), IMM(2));  JUMP_LT(HAS_NOT_ENOUGH_ARGS_APPLY);  CMP(IND(FPARG(2)),T_CLOSURE);  JUMP_NE(NOT_VALID_ARG_APPLY);    MOV(R1,IMM(3));  MOV(R0,FPARG(3));    CMP(IND(R0),T_NIL);  JUMP_EQ(EMPTY_APPLY);    PUSH_REGULAR_PARAMS_APPLY:  CMP(IND(R0),T_NIL);  JUMP_EQ(END_PARAMS_APPLY);  CMP(IND(R0),T_PAIR);  JUMP_EQ(PUSH_LIST_PARAMS_APPLY);  PUSH(R0);  INCR(R1);  MOV(R0,FPARG(R1));  JUMP(PUSH_REGULAR_PARAMS_APPLY);    PUSH_LIST_PARAMS_APPLY:  CMP(IND(R0),T_PAIR);  JUMP_NE(END_PARAMS_APPLY);  PUSH(INDD(R0,IMM(1)));  MOV(R0,INDD(R0,IMM(2)));  JUMP(PUSH_LIST_PARAMS_APPLY);    END_PARAMS_APPLY:  MOV(R1,IMM(-1));  MOV(R2,SP);  SUB(R2,FP);  SUB(R2,IMM(5));    REVERSE_LOOP_APPLY:  CMP(R1,R2);  JUMP_GE(END_REVERSE_APPLY);  MOV(R3,STARG(R1));  MOV(STARG(R1),STARG(R2));  MOV(STARG(R2),R3);  INCR(R1);  DECR(R2);  JUMP(REVERSE_LOOP_APPLY);    END_REVERSE_APPLY:  MOV(R1,SP);  SUB(R1,FP);  SUB(R1,IMM(3));  PUSH(R1);  MOV(R2,FPARG(2));  PUSH(INDD(R2,IMM(1)));  CALLA(INDD(R2,IMM(2)));    DROP(IMM(1));   POP(R1);  DROP(R1);     POP(R3);  POP(R2);  POP(R1);  POP(FP);  RETURN;    EMPTY_APPLY:  PUSH(IMM(0));  MOV(R2,FPARG(2));  PUSH(INDD(R2,IMM(1)));  CALLA(INDD(R2,IMM(2)));    DROP(IMM(2));     POP(R3);  POP(R2);  POP(R1);  POP(FP);  RETURN;    NOT_VALID_ARG_APPLY:  CALL(ERROR_NOT_VALID_ARG);    HAS_NOT_ENOUGH_ARGS_APPLY:  CALL(ERROR_NOT_ENOUGH_ARGS);