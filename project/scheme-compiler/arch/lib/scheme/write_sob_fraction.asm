/* scheme/write_sob_fraction.asm
 * Take a pointer to a Scheme fraction object, and 
 * prints (to stdout) the character representation
 * of that object.
 */

 WRITE_SOB_FRACTION:
  PUSH(FP);
  MOV(FP, SP);
  PUSH (R1);
  MOV(R1, FPARG(0));
  MOV(R0, INDD(R1, 1));
  PUSH(R0);
  CALL(WRITE_INTEGER);
  DROP(1);
  PUSH(IMM('/'));
  CALL(PUTCHAR);
  DROP(1);
  MOV(R0, INDD(R1, 2));
  PUSH(R0);
  CALL(WRITE_INTEGER);
  DROP(1);
  POP(R1);
  POP(FP);
  RETURN;

