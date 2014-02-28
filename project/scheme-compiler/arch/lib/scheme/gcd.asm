GCD:
  PUSH(FP);
  MOV(FP, SP);
  
  PUSH (R1);
  PUSH (R2);
  PUSH (R3);
  PUSH (R4);
  
  MOV (R1,FPARG(1));
  MOV (R2,FPARG(2));
  MOV (R3,R1);
  MOV (R4,R2);
  
  CMP(R1,R2);
  JUMP_EQ(GCD_RETURN_R1);
  CMP(R1,0);
  JUMP_EQ(GCD_RETURN_R2);
  CMP(R2,0);
  JUMP_EQ(GCD_RETURN_R1);
 
  
  
  
  
  GCD_RETURN_R1:
  MOV (R0,R1);
  JUMP (GCD_END);
  
  GCD_RETURN_R2:
  MOV (R0,R2);
  JUMP (GCD_END);
  
  
  GCD_END:
  POP(R4);
  POP(R3);
  POP(R2);
  POP(R1);
  MOV(SP,FP);
  POP(FP);
  RETURN;
