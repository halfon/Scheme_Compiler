/* puts in r0 the string that represent the symbol */

 STRING_SYMBOL:
  PUSH(FP);
  MOV(FP, SP);
  
  CMP(FPARG(1), IMM(1));
  JUMP_LT(HAS_NO_ARGS_STRING_SYMBOL);
  JUMP_GT(TOO_MANY_ARGS_STRING_SYMBOL);
  CMP(IND(FPARG(2)),T_STRING);
  JUMP_NE(NOT_VALID_ARG_STRING_SYMBOL);
  
  PUSH (FPARG(2));
  CALL (find_or_create_bucket);
  DROP(1);
  // now in r0 there is a pointer to a bucket
  MOV (IND(R0),FPARG(2));
  //now the bucket has the string.
  //just to point a symbol to the bucket
  
  PUSH(R1);
  PUSH(R2);
  PUSH(R3);
  MOV(R3,R0);
  MOV(R1,1);
  MOV(R2,IND(0));
  STRING_SYMBOL_KEEP_LOOKING:
  CMP (R2,0);
  JUMP_EQ (STRING_SYMBOL_CREATE_NEW_SYMBOL);
  CMP(IND(R1),T_SYMBOL);
  JUMP_NE(STRING_SYMBOL_CHECK_NEXT_CELL);
  CMP(INDD(R1,1),R3);
  JUMP_EQ(STRING_SYMBOL_FOUND_A_MATCH);
  STRING_SYMBOL_CHECK_NEXT_CELL:
  INCR(R1);
  DECR(R2);
  JUMP(STRING_SYMBOL_KEEP_LOOKING);
  STRING_SYMBOL_CREATE_NEW_SYMBOL:
  PUSH(2);
  CALL (MALLOC);
  DROP(1);
  MOV(IND(R0),T_SYMBOL);
  MOV(INDD(R0,1),R3);
  MOV(R1,R0);
  STRING_SYMBOL_FOUND_A_MATCH:
  MOV(R0,R1);
  POP(R3);
  POP(R2);
  POP(R1);
  POP(FP);
  RETURN;
  
  NOT_VALID_ARG_STRING_SYMBOL:
  CALL(ERROR_NOT_VALID_ARG);
  
  HAS_NO_ARGS_STRING_SYMBOL:
  CALL(ERROR_NOT_ENOUGH_ARGS);
  
  TOO_MANY_ARGS_STRING_SYMBOL:
  CALL(ERROR_TOO_MANY_ARGS);