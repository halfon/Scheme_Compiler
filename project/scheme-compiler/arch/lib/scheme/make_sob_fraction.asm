/* scheme/make_sob_fraction.asm
 * Takes two integers, and place the corresponding Scheme object in R0
 * first push the dome (מכנה) and then push the mone (מונה)
 * fparg(0) = מונה
 * fparg(1)= מכנה
 */

 MAKE_SOB_FRACTION:
  PUSH(FP);
  MOV(FP, SP);
  PUSH(IMM(3));
  CALL(MALLOC);
  DROP(1);
  CMP(FPARG(0), IMM(0));
  JUMP_LT(MAYBE_FRAC);
  CMP(FPARG(1), IMM(0));
  JUMP_LT(REPLACE_FRAC);
  L_NORMAL:
  MOV(IND(R0), T_FRACTION);
  MOV(INDD(R0, 1), FPARG(0));
  MOV(INDD(R0, 2), FPARG(1));
  POP(FP);
  RETURN;

  MAYBE_FRAC:
  CMP(FPARG(1), IMM(0));
  JUMP_GT(L_NORMAL);
  REPLACE_FRAC:
  MUL(FPARG(0),IMM(-1));
  MUL(FPARG(1),IMM(-1));
  MOV(IND(R0), T_FRACTION);
  MOV(INDD(R0, 1), FPARG(0));
  MOV(INDD(R0, 2), FPARG(1));
  POP(FP);
  RETURN;