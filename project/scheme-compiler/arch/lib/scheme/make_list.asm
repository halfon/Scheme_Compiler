/* scheme/make_list.asm
 * Gets a pointer to a non-empty proper list, and duplicate it to a new list which will be in R0
 */

 MAKE_LIST:
  PUSH(FP);
  MOV(FP, SP);
  PUSH(R1); // ישמור את הרשימה הנצברת
  PUSH(R2); // יצביע לזוג הבא ברשימה הקיימת
  PUSH(R3); // יצביע לזוג האחרון ברשימה הנצברת
  
  CMP(FPARG(1), IMM(1));
  JUMP_LT(HAS_NO_ARGS_LIST);
  JUMP_GT(TOO_MANY_ARGS_LIST);
  CMP(IND(FPARG(2)),IMM(T_PAIR));
  JUMP_NE(NOT_VALID_ARG_LIST);
  
  MOV(R2,FPARG(2));
  PUSH(IMM(2));
  PUSH(INDD(R2,1));
  CALL(MAKE_SOB_PAIR);
  DROP(2);
  MOV(R1,R0);
  MOV(R3,R0);
  CMP(INDD(R2,2),IMM(2));
  JUMP_EQ(FINISH_MAKE_LIST);
  
  MAKE_LIST_LOOP:
  MOV(R2,INDD(R2,2));
  PUSH(IMM(2));
  PUSH(INDD(R2,1));
  CALL(MAKE_SOB_PAIR);
  DROP(2);
  MOV(INDD(R3,2),R0);
  MOV(R3,INDD(R3,2));
  CMP(INDD(R2,2),IMM(2));
  JUMP_EQ(FINISH_MAKE_LIST);
  JUMP(MAKE_LIST_LOOP);
  
  FINISH_MAKE_LIST:
  MOV(R0,R1);
  POP(R3);
  POP(R2);
  POP(R1);
  POP(FP);
  RETURN;

  HAS_NO_ARGS_LIST:
  CALL(ERROR_NOT_ENOUGH_ARGS);
  
  TOO_MANY_ARGS_LIST:
  CALL(ERROR_TOO_MANY_ARGS);
  
  NOT_VALID_ARG_LIST:
  CALL(ERROR_NOT_VALID_ARG);