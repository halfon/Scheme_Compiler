/* plus.asm * Computes the sum of variadic number of integers: R0 <- ARG[0] + ARG[1] +... */ PLUS:  PUSH(FP);  MOV(FP, SP);    MOV(R0,FPARG(3));  SHOW("",FPARG(1));  MOV(R0,INDD(R0,1));  MOV(R1,FPARG(2));  SHOW("",R1);  MOV(R1,INDD(R1,1));      ADD (R0,R1);  PUSH (R0);  CALL (MAKE_SOB_INTEGER);  DROP(1);  MOV (SP,FP);  POP(FP);  RETURN;