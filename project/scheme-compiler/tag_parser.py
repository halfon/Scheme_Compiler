# coding=utf8
import reader
import sexprs



class lableCount:
    count=0
    @staticmethod
    def newLableNumber():
        lableCount.count=lableCount.count+1
        return lableCount.count

class genSym:
    count=0
    @staticmethod
    def newGenSym():
        res="@"+'G'+str(genSym.count)
        genSym.count=genSym.count+1
        return sexprs.Symbol(res)

def checkOr(s_exp):
    if isinstance(s_exp,sexprs.Pair):
        if isinstance(s_exp.second,sexprs.Nil):
            return AbstractSchemeExpr.parse_after_reader(s_exp.first)
    else:
        return AbstractSchemeExpr.parse_after_reader(sexprs.false())
    return Or(s_exp)

def isProperList(l):
    if isinstance(l,sexprs.Nil):
        return True
    elif isinstance(l,sexprs.Pair):
        return isProperList(l.second)
    else:
        return False

def printArray(list):
    temp=""
    for x in list:
        temp=temp + str(x)+ ' '
    temp=temp[0:-1]
    return temp

def condToIf (s_exp):
    if isinstance(s_exp,sexprs.Pair):
        if isinstance(s_exp.second, sexprs.Nil):
            if isinstance(s_exp.first.first,sexprs.Symbol)and s_exp.first.first.string=="ELSE":
                return s_exp.first.second.first
            return sexprs.Pair(sexprs.Symbol("IF"), sexprs.Pair(s_exp.first.first, sexprs.Pair(s_exp.first.second.first, sexprs.Nil())))
        return sexprs.Pair(sexprs.Symbol("IF"),sexprs.Pair(s_exp.first.first,sexprs.Pair(s_exp.first.second.first,sexprs.Pair(
            sexprs.Pair(sexprs.Symbol("COND"),s_exp.second)
            ,sexprs.Nil()))))

def andToIf(s_exp):
    if isinstance(s_exp,sexprs.Nil):
        return sexprs.true()
    if isinstance(s_exp,sexprs.Pair):
        if isinstance(s_exp.second,sexprs.Nil):
            return s_exp.first
    return sexprs.Pair(sexprs.Symbol("IF"),sexprs.Pair(s_exp.first,sexprs.Pair(
        sexprs.Pair(sexprs.Symbol("AND"),s_exp.second)
        ,sexprs.Pair(sexprs.false(),sexprs.Nil()))))

def letToApplic(s_exp):
    param=[]
    values=[]
    temp=s_exp.first
    while isinstance(temp,sexprs.Pair):
        param.append(temp.first.first)
        values.append(temp.first.second.first)
        temp=temp.second
    body=s_exp.second.first
    s_param=sexprs.Nil()
    for x in reversed (param):
        s_param=sexprs.Pair(x,s_param)
    s_values=sexprs.Nil()
    for y in reversed(values):
        s_values=sexprs.Pair(y,s_values)
    return sexprs.Pair(
        sexprs.Pair(sexprs.Symbol('LAMBDA'), sexprs.Pair(s_param, sexprs.Pair(body, sexprs.Nil()))),
        s_values
    )

def letStarToApplic(s_exp):
    if isinstance(s_exp, sexprs.Pair) and isinstance(s_exp.second, sexprs.Pair):
        body = s_exp.second.first
        if isinstance(s_exp.first, sexprs.Nil):
            return body
        if isinstance(s_exp.first, sexprs.Pair):
            param = s_exp.first.first.first
            value = s_exp.first.first.second.first
            rest = s_exp.first.second
            return sexprs.Pair(
                                sexprs.Pair(sexprs.Symbol("LAMBDA"), sexprs.Pair(
                                        sexprs.Pair(param, sexprs.Nil())
                                    , sexprs.Pair(
                                        sexprs.Pair(sexprs.Symbol("LET*"), sexprs.Pair(
                                            rest
                                            , sexprs.Pair(
                                            body
                                            , sexprs.Nil())))
                                    , sexprs.Nil())))
                            , sexprs.Pair(
                                value
                            , sexprs.Nil()))

def letToYagApplic(s_exp):
    body=s_exp.second.first
    if isinstance(s_exp.first,sexprs.Nil):
        return body
    generatedSymbol=genSym.newGenSym()
    param=[];
    values=[];
    temp=s_exp.first
    while isinstance(temp,sexprs.Pair):
        param.append(temp.first.first)
        values.append(temp.first.second.first)
        temp=temp.second
    s_param=sexprs.Nil()
    for x in reversed (param):
        s_param=sexprs.Pair(x,s_param)
    s_param=sexprs.Pair(generatedSymbol,s_param)
    s_values=[]
    for y in values:
        s_values.append(y)
    firstLambda=sexprs.Pair(
        sexprs.Symbol("LAMBDA"),
        sexprs.Pair(
            s_param,
            sexprs.Pair(
                body,
                sexprs.Nil()
            )
        )
    )
    list_of_lambdas=[]
    for x in s_values:
        list_of_lambdas.append(
            sexprs.Pair(
        sexprs.Symbol("LAMBDA"),
        sexprs.Pair(
            s_param,
            sexprs.Pair(
                x,
                sexprs.Nil(
                )
                )))
        )
    pairedListofLambdas=sexprs.Nil()
    for x in reversed(list_of_lambdas):
        pairedListofLambdas=sexprs.Pair(x,pairedListofLambdas)
    pairedListofLambdas=sexprs.Pair(firstLambda,pairedListofLambdas)

    return sexprs.Pair(
        sexprs.Symbol("YAG"),
            pairedListofLambdas
    )

def checkIfParam (var,paramList):
    for i in paramList:
        if var.isequal(i):
            return paramList.index(i)
    return None

def checkIfBound (var,boundList):
    for i in boundList:
        for j in boundList[boundList.index(i)]:
            if var.isequal(j):
                return boundList.index(i) , boundList[boundList.index(i)].index(j)
    return None,None

def boundCopy(b,p):
    newB=[]
    newB.append(p)
    for x in b:
        newB.append(x)
    return newB

def paramCopy(p):
    newP=[]
    if isinstance(p,list):
        for x in p:
            newP.append(x)
    else:
        newP.append(p)
    return newP

class AbstractSchemeExpr:
    @staticmethod
    def macro_exp(s_exp):
        if isinstance(s_exp,sexprs.Pair):
            if isinstance(s_exp.first,sexprs.Symbol):
                if s_exp.first.string in syntaticWords:
                    return syntaticWords[s_exp.first.string](s_exp.second)
        return s_exp

    @staticmethod
    def Lambdacheck(s_exp):
        if isinstance(s_exp.first,sexprs.Pair):
            if isProperList(s_exp.first):
                return LambdaSimple(s_exp)
            else:
                return LambdaOpt(s_exp)
        elif isinstance (s_exp.first,sexprs.Nil):
                return LambdaSimple(s_exp)
        else:
            return LambdaVar(s_exp)

    @staticmethod
    def parse (str):
        s_exp , remain =sexprs.AbstractSexpr.readFromString(str)
        return AbstractSchemeExpr.parse_after_reader(s_exp),remain

    @staticmethod
    def parse_after_reader(s_exp):
        s_exp=AbstractSchemeExpr.macro_exp(s_exp)
        s_exp=AbstractSchemeExpr.macro_exp(s_exp)
        if isinstance(s_exp,sexprs.Pair):
            if isinstance(s_exp.first,sexprs.Symbol):
                if s_exp.first.string in schemeWords:
                    return schemeWords[s_exp.first.string](s_exp.second)
                else:
                    return Applic(s_exp)
            if isinstance(s_exp,sexprs.Pair):
                if isinstance(s_exp.first,sexprs.Pair):
                    if isinstance(s_exp.first.first,sexprs.Symbol):
                        if s_exp.first.first.string == "LAMBDA":
                            if isinstance(s_exp.first.second,sexprs.Pair):
                                if isinstance(s_exp.first.second.first,sexprs.Nil):
                                    if isinstance(s_exp.first.second.second,sexprs.Pair):
                                        return AbstractSchemeExpr.parse_after_reader(s_exp.first.second.second.first)
                return Applic(s_exp)
        elif isinstance(s_exp,sexprs.Symbol):
            return Variable(s_exp)
        elif isinstance (s_exp, sexprs.AbstractBoolean) or isinstance(s_exp, sexprs.AbstractNumber) or isinstance(s_exp,sexprs.String) or isinstance(s_exp,sexprs.Char):
            return Constant(s_exp)

    def __str__(self):
        return self.accept(AsStringVisitor)

    def debruijn(self,b=[],p=[]):
        if isinstance (self,AbstractLambda):
            self.env_size=len(b)
            new_b=boundCopy(b,p)
            new_p=paramCopy(self.param)
            if isinstance(self,LambdaOpt):
                new_p.append(self.opt)
            self.body=self.body.debruijn(new_b,new_p)

            return self
        elif isinstance(self,Variable):
            pMinor=checkIfParam(self,p)
            if pMinor != None:
                return VarParam(self,pMinor)
            else:
                bMajor,bMinor=checkIfBound(self,b)
                if bMajor!=None and bMinor!=None:
                    return VarBound (self,bMajor,bMinor)
                else:
                    return VarFree(self)
        else:
            if isinstance(self,IfThenElse):
                self.Condition=self.Condition.debruijn(b,p)
                self.Then=self.Then.debruijn(b,p)
                self.Else=self.Else.debruijn(b,p)
                return self
            elif isinstance (self,Def):
                #self.var=self.var.debruijn()
                #if (define x 4)should give x freevar
                self.body=self.body.debruijn(b,p)
                return self
            elif isinstance(self,Constant):
                return self
            elif isinstance(self,Applic):
                self.applic=self.applic.debruijn(b,p)
                newparam=[]
                for x in self.param:
                    temp=x.debruijn(b,p)
                    newparam.append(temp)
                self.param=newparam
                return self
            elif isinstance(self,Or):
                newparam=[]
                for x in self.param:
                    temp=x.debruijn(b,p)
                    newparam.append(temp)
                self.param=newparam
                return self

    def annotateTC(self,isTP=False):
        if isinstance(self,Variable) or isinstance(self,Constant):
            return self
        elif isinstance(self,Applic):
            self.applic=self.applic.annotateTC()
            newParam=[]
            for x in self.param:
                temp=x.annotateTC()
                newParam.append(temp)
            self.param=newParam
            if isTP:
                return ApplicTP(self)
            else:
                return self
        elif isinstance(self,Or):
            newparam=[]
            for x in self.param:
                if self.param.index(x) == len(self.param):
                    newparam.append(x.annotateTC(isTP))
                else:
                    newparam.append(x.annotateTC())
            self.param=newparam
            return self
        elif isinstance(self,IfThenElse):
            self.Condition=self.Condition.annotateTC()
            self.Then=self.Then.annotateTC(isTP)
            self.Else=self.Else.annotateTC(isTP)
            return self
        elif isinstance(self,Def):
            self.body=self.body.annotateTC()
            return self
        elif isinstance(self,AbstractLambda):
            self.body=self.body.annotateTC(True)
            return self
        else:
            return self

    def semantic_analysis(self):
        return self.debruijn()\
        .annotateTC()

    def  code_gen(self):
        return self.accept(CodeGenVisitor)

class CodeGenVisitor():
    def visitIfThenElse(self):
        #todo find what to compare the if condtion with
        res = '''BEGIN_LOCAL_LABELS ifBegin, ifThen, ifElse, ifEnd;
                ifBegin:
                %s
                CMP(R0,FALSE_CONSTANT);
                JUMP_EQ (ifElse);
                ifThen:
                %s
                JUMP(ifEnd);
                ifElse:
                %s
                ifEnd:
                NOP;
                END_LOCAL_LABELS;
                '''%(self.Condition.code_gen(),self.Then.code_gen(),self.Else.code_gen())
        return res
    def visitDef(self):
        res='''
            PUSH(R1);
            //body code_gen:
            %s
            MOV (R1,R0);
            //go on list of bucket and search a string that matches the var string
            //if fount replace its data with define data
            //if not fount create a new bucket with the currect string and the def data.

            PUSH (%d); //push the represnted string.
            CALL (find_or_create_bucket);
            DROP(1);
            //now we have a bucket we put the string and the data inside.
            MOV (IND(R0),%d); // put string in place
            MOV (INDD(R0,1),R1); // pointer to data
            //make the symbol in the const table to point the bucket:
            MOV (IND(%d),R0);
            //put void in r0
            MOV (R0, 1);
            POP(R1);
        '''%(self.body.code_gen(),Const_table.const_table[self.var.ref+1] , Const_table.const_table[self.var.ref+1],self.var.ref+1)
        return res
    def visitVar(self):
        pass
    def visitVarFree(self):
        res='''
        MOV (R0,IND(%d));
        MOV (R0,INDD(R0,1));
        '''%(self.Var.ref +1)
        return res
    def visitVarParam(self):
        res='''
        MOV (R0,FPARG(%d));
        '''%(self.minor + 2)
        return res
    def visitVarBound(self):
        res='''
        MOV (R0,FPARG(0));
        MOV (R0, INDD (R0,%d));
        MOV (R0, INDD (R0,%d));
        '''%(self.major,self.minor)
        return res
    def visitConst(self):
        res=""
        if isinstance(self.con,sexprs.Integer):
            res ='MOV (R0 , IMM(%d));'%(self.con.ref)
        elif isinstance(self.con,sexprs.Fraction):
            res ='MOV (R0 , IMM(%d));'%(self.con.ref)
        elif isinstance(self.con,sexprs.AbstractBoolean):
            if self.con.value == True :
                res = "MOV (R0,IMM(3));"
            else:
                res = "MOV (R0,IMM(5));"
        elif isinstance (self.con,sexprs.String):
            res = '''MOV (R0 , %d)'''%(self.con.ref)
        elif isinstance (self.con,sexprs.Char):
            res = '''MOV (R0 , %d)'''%(self.con.ref)
        elif isinstance (self.con,sexprs.Symbol):
            #lnum= lableCount.newLableNumber()
            #todo change the ref here to bucket
            # res = '''
            #         MOV (R0 , %d);
            #         MOV (R0 , INDD(R0,1));
            #         '''%(self.con.ref)
            res = '''MOV (R0 , %d)'''%(self.con.ref)
        elif isinstance (self.con,sexprs.Vector):
            res = '''MOV (R0 , %d)'''%(self.con.ref)
        elif isinstance (self.con,sexprs.Pair):
            res = '''MOV (R0 , %d)'''%(self.con.ref)
        elif isinstance (self.con,sexprs.Nil):
            res = '''MOV (R0 , %d)'''%(self.con.ref)
        else:
            res = "MOV (R0,IMM(1));\n"
        return res
    def visitLambdaSimple(self):
        lnum= lableCount.newLableNumber()
        res = '''
        JUMP (LambdaSimple_ClosCreation_%d);
        LambdaSimple_Body_%d:
        PUSH(FP);
        MOV(FP,SP);
        %s
        MOV(SP,FP);
        POP(FP);
        RETURN;

        LambdaSimple_ClosCreation_%d:
        PUSH(R1);
        PUSH(R2);
        PUSH(R3);
        PUSH(R4);
        //extend the env:
        PUSH (%d); // new env size;
        CALL (MALLOC);
        DROP(1);
        // now r0 holdes a pointer to the new env
        MOV (R1,R0);
        PUSH (%d); // old env size
        PUSH (FPARG(0)); // push old env
        PUSH (R0);  // new env address
        CALL (COPY_ENV);
        DROP(3);
        MOV(R1,R0);
        // now r1 holdes a pointer to the new env with the old env copied to it.
        //now we need to malloc a new array and copy the params from the stack to it.
        PUSH (FPARG(1));
        CALL (MALLOC);
        DROP (1);
        // now r0 holds a pointer to array of size params;
        MOV (IND(R1),0);
        MOV (R2,FPARG(1)); // R2 is the number of params on stack
        MOV (R3,2); // R3 is the first param;
        MOV (R4,0); // R4 is the location to insert the param on the array
        env_param_copy_%d:
        CMP(R2,0);
        JUMP_EQ(env_param_copy_end_%d);
        MOV (INDD(R0,R4),FPARG(R3));
        MOV (IND(R1),R0);
        DECR (R2);
        INCR (R3);
        INCR (R4);
        JUMP (env_param_copy_%d);
        env_param_copy_end_%d:
        PUSH (LABEL(LambdaSimple_Body_%d));
        PUSH (R1);
        CALL (MAKE_SOB_CLOSURE);
        DROP(2);

        POP(R4);
        POP(R3);
        POP(R2);
        POP(R1);
        LambdaSimple_end_%d:
        '''%(lnum,lnum,self.body.code_gen(),lnum,self.env_size +1,self.env_size,lnum,lnum,lnum,lnum,lnum,lnum )

        return res

    def visitLambdaOpt(self):
        lnum= lableCount.newLableNumber()
        res = '''
        JUMP (LambdaOpt_ClosCreation_%d);
        LambdaOpt_Body_%d:
        PUSH(FP);
        MOV(FP,SP);
        //need to fix the stack
        PUSH(R1);
        PUSH(R2);
        PUSH(R3);
        PUSH(R4);
        PUSH(R5);
        MOV (R0, IMM(2)); // put nil in r0
        MOV (R2,FPARG(1)); // now r2 has the number of arguments the applic got
        MOV (R3,R2);
        INCR (R3); // r3 hold the position fparg(r3) from the place we need to make a list
        MOV (R4,R3); //R4 hold same info for later use
        SUB (R2,%d); // r2 has the number of arguments to chain in a list
        MOV (R5,R2); //R5 HOLD the number of arguments to chain in a list for later use
        LambdaOpt_optional_loop_start_%d:
        CMP (R2,0);
        JUMP_EQ(LambdaOpt_optional_loop_end_%d);
        PUSH (R0);
        PUSH (FPARG(R3));
        CALL (MAKE_SOB_PAIR);
        DROP(2);
        DECR(R3);
        DECR(R2);
        JUMP (LambdaOpt_optional_loop_start_%d);
        LambdaOpt_optional_loop_end_%d:
        //now r0 hold a pointer to a list of pairs to push on the stack
        PUSH(R0);
        MOV (R1,%d); //R1 holds the amount of param on the stack
        MOV (R3,R1);
        INCR (R3); // R3 hold the position fparg(r3) from the place we need to copy params...
        ADD (R1,IMM(9));
        LambdaOpt_param_loop_start_%d:
        CMP(R1,0);
        JUMP_EQ(LambdaOpt_param_loop_end_%d);
        PUSH(FPARG(R3));
        DECR(R3);
        DECR(R1);
        JUMP (LambdaOpt_param_loop_start_%d);
        LambdaOpt_param_loop_end_%d:
        //now all the new frame is at top of the stack.. all we need to do is copy it to bottom of the stack.
        //R4 hold the number of fparg to copy to. and so R0;
        //now r1 will hold the amount of things to copy
        MOV (R0,R4);
        MOV (R2,IMM(-8)); //R2 HOLD the place the new frame start in.. always -8 (because of the pushes of the R1..R4)..
        MOV (R1,%d); //r1 has number of params.
        INCR(R1); // NOW it take into account the list
        ADD (R1,9); // IN ADDITION 8 MORE THINGS TO CONSIDER.

        LambdaOpt_frame_relocate_loop_start_%d:
        CMP (R1,0);
        JUMP_EQ (LambdaOpt_frame_relocate_loop_end_%d);
        MOV (FPARG(R4),FPARG(R2));
        DECR (R4);
        DECR (R2);
        DECR (R1);
        JUMP (LambdaOpt_frame_relocate_loop_start_%d);
        LambdaOpt_frame_relocate_loop_end_%d:

        MOV (R3,%d);
        ADD (R3,10);
        DECR (R5);  //R5 hold the number of optional arguments and we need to decr it by 1.
        ADD (R3,R5);
        DROP(R3);
        SUB (FP,R5);
        //DECR(FP);
        MOV (FPARG(1),%d);
        '''%(lnum,lnum,len(self.param),lnum,lnum,lnum,lnum,len(self.param),lnum,lnum,lnum,lnum,len(self.param),lnum,lnum,lnum,lnum,len(self.param),len(self.param)+1) + \
        '''
        LambdaOpt_body_start_%d:
        POP(R5);
        POP(R4);
        POP(R3);
        POP(R2);
        POP(R1);
        %s
        MOV(SP,FP);
        POP(FP);
        RETURN;

        LambdaOpt_ClosCreation_%d:
        PUSH(R1);
        PUSH(R2);
        PUSH(R3);
        PUSH(R4);
        //extend the env:
        PUSH (%d); // new env size;
        CALL (MALLOC);
        DROP(1);
        // now r0 holdes a pointer to the new env
        MOV (R1,R0);
        PUSH (%d); // old env size
        PUSH (FPARG(0)); // push old env
        PUSH (R0);  // new env address
        CALL (COPY_ENV);
        DROP(3);
        MOV(R1,R0);
        // now r1 holdes a pointer to the new env with the old env copied to it.
        //now we need to malloc a new array and copy the params from the stack to it.
        PUSH (FPARG(1));
        CALL (MALLOC);
        DROP (1);
        // now r0 holds a pointer to array of size params;
        MOV (IND(R1),0);
        MOV (R2,FPARG(1)); // R2 is the number of params on stack
        MOV (R3,2); // R3 is the first param;
        MOV (R4,0); // R4 is the location to insert the param on the array
        env_param_copy_%d:
        CMP(R2,0);
        JUMP_EQ(env_param_copy_end_%d);
        MOV (INDD(R0,R4),FPARG(R3));
        MOV (IND(R1),R0);
        DECR (R2);
        INCR (R3);
        INCR (R4);
        JUMP (env_param_copy_%d);
        env_param_copy_end_%d:
        PUSH (LABEL(LambdaOpt_Body_%d));
        PUSH (R1);
        CALL (MAKE_SOB_CLOSURE);
        DROP(2);

        POP(R4);
        POP(R3);
        POP(R2);
        POP(R1);
        LambdaOpt_end_%d:
        NOP;
        '''%(lnum,self.body.code_gen(),lnum,self.env_size +1,self.env_size,lnum,lnum,lnum,lnum,lnum,lnum )
        return res
    def visitLambdaVar(self):
        lnum= lableCount.newLableNumber()
        res = '''
        JUMP (LambdaVar_ClosCreation_%d);
        LambdaVar_Body_%d:
        PUSH(FP);
        MOV(FP,SP);
        //need to fix the stack
        PUSH(R1);
        MOV (R1,FPARG(1));
        CMP(R1,0);
        JUMP_NE(LamdaVar_stack_fix_normal_%d);
        //equal means 0 args.
        PUSH (2); //PUSH NIL;
        PUSH (IMM(1));
        PUSH (FPARG(0));
        PUSH (FPARG(-1));
        PUSH (FPARG(-2));
        PUSH (FPARG(-3));
        //now the new stack start at fparg(-4);
        MOV(FPARG(2),FPARG(-4));
        MOV(FPARG(1),FPARG(-5));
        MOV(FPARG(0),FPARG(-6));
        MOV(FPARG(-1),FPARG(-7));
        MOV(FPARG(-2),FPARG(-8));
        MOV(FPARG(-3),FPARG(-9));
        DROP(6);
        JUMP(LambdaVar_body_start_%d);
        LamdaVar_stack_fix_normal_%d:
        PUSH (R2);
        PUSH (R3);
        PUSH (R4);
        MOV(R4,2);
        MOV (R3,R1);
        ADD(R4,R3);
        DECR(R4);
        MOV(R2,2);
        PUSH (2); // PUSH NIL;
        PUSH (FPARG(R4));
        CALL (MAKE_SOB_PAIR);
        DROP(2);
        DECR(R1);
        LamdaVar_stack_loop_start_%d:
        CMP(R1,0);
        JUMP_EQ(LamdaVar_stack_loop_end_%d);
        INCR(R2);
        DECR(R4);
        DECR(R1);
        PUSH (R0);
        PUSH (FPARG(R4));
        CALL (MAKE_SOB_PAIR);
        DROP(2);
        JUMP (LamdaVar_stack_loop_start_%d);
        LamdaVar_stack_loop_end_%d:
        MOV (FPARG(R2),R0);
        DECR(R2);
        MOV (FPARG(R2),1);
        DECR(R2);
        MOV (FPARG(R2),FPARG(0));
        DECR(R2);
        MOV (FPARG(R2),FPARG(-1));
        DECR(R2);
        MOV (FPARG(R2),FPARG(-2));
        DECR(R2);
        MOV (FPARG(R2),FPARG(-3));
        DECR(R2);
        MOV (FPARG(R2),FPARG(-4));
        DECR(R2);
        MOV (FPARG(R2),FPARG(-5));
        DECR(R2);
        MOV (FPARG(R2),FPARG(-6));
        ADD(R3,-1);
        DROP(R3);
        POP (R4);
        POP(R3);
        POP(R2);
        MOV(FP,SP);
        DECR(FP);
        POP(R1);
        //end of fixing stack
        LambdaVar_body_start_%d:
        %s
        MOV(SP,FP);
        POP(FP);
        RETURN;

        LambdaVar_ClosCreation_%d:
        PUSH(R1);
        PUSH(R2);
        PUSH(R3);
        PUSH(R4);;
        //extend the env:
        PUSH (%d); // new env size;
        CALL (MALLOC);
        DROP(1);
        // now r0 holdes a pointer to the new env
        MOV (R1,R0);
        PUSH (%d); // old env size
        PUSH (FPARG(0)); // push old env
        PUSH (R0);  // new env address
        CALL (COPY_ENV);
        DROP(3);
        MOV(R1,R0);
        // now r1 holdes a pointer to the new env with the old env copied to it.
        //now we need to malloc a new array and copy the params from the stack to it.
        PUSH (FPARG(1));
        CALL (MALLOC);
        DROP (1);
        // now r0 holds a pointer to array of size params;
        MOV (IND(R1),0);
        MOV (R2,FPARG(1)); // R2 is the number of params on stack
        MOV (R3,2); // R3 is the first param;
        MOV (R4,0); // R4 is the location to insert the param on the array
        env_param_copy_%d:
        CMP(R2,0);
        JUMP_EQ(env_param_copy_end_%d);
        MOV (INDD(R0,R4),FPARG(R3));
        MOV (IND(R1),R0);
        DECR (R2);
        INCR (R3);
        INCR (R4);
        JUMP (env_param_copy_%d);
        env_param_copy_end_%d:
        PUSH (LABEL(LambdaVar_Body_%d));
        PUSH (R1);
        CALL (MAKE_SOB_CLOSURE);
        DROP(2);

        POP(R4);
        POP(R3);
        POP(R2);
        POP(R1);
        LambdaVar_end_%d:
        '''%(lnum,lnum,lnum,lnum,lnum,lnum,lnum,lnum,lnum,lnum,self.body.code_gen(),lnum,self.env_size +1,self.env_size,lnum,lnum,lnum,lnum,lnum,lnum )
        return res

    def visitOr(self):
        res=''
        res+= \
'''                BEGIN_LOCAL_LABELS orBegin, orEnd;
                orBegin:
                '''
        for x in self.param[0:-1]:
            res = res + x.code_gen()
            res+='''
                CMP(R0,FALSE_CONSTANT);
                JUMP_NE (orEnd);
                '''
        res = res + self.param[-1].code_gen()+'''
                orEnd:
                NOP;
                END_LOCAL_LABELS;
             '''
        return res
    def visitApplic(self):
        lnum= lableCount.newLableNumber()
        res="//applic no. %d begin here\n"%(lnum)
        for x in reversed(self.param):
            res += x.code_gen()+'\n'
            res += "PUSH(R0);\n"
        res += "PUSH(%d);"%(len(self.param))
        res += self.applic.code_gen()
        res += '''
        PUSH (INDD(R0,1));
        CALLA (INDD(R0,2));
        DROP(1); //DROP the env
        POP(R15); //now r1 has the arg size
        DROP(R15);
        // applic no. %d end here
        '''%(lnum)
        return res
    def visitApplicTP(self):
        lnum= lableCount.newLableNumber()
        res="//applicTP no. %d start here\n"%(lnum)
        res+='''
        '''
        for x in reversed(self.param):
            res += x.code_gen()+'\n'
            res += "PUSH(R0);\n"
        res += "PUSH(%d);"%(len(self.param))
        res+=self.applic.code_gen()
        res+='''
        PUSH(INDD(R0,1));
        PUSH(FPARG(-1)); // PUSH RET ADRESS
        PUSH(R15);
        PUSH(R14);
        PUSH(R13);
        PUSH(R12);
        PUSH(R11);
        MOV (R15,FPARG(-2)); // SAVE FP OF OLD FRAME

        MOV (R14,FPARG(1));
        MOV(R11,R14);
        ADD(R11,4);
        INCR(R14);
        MOV(R13,%d);
        ADD(R13,3);
        ADD(R13,5);
        MOV (R12,-3);
        APPLIC_TP_LOOP_START_%d:
        CMP (R13,0);
        JUMP_EQ(APPLIC_TP_LOOP_END_%d);
        MOV(FPARG(R14),FPARG(R12));
        DECR(R14);
        DECR(R12);
        DECR(R13);
        JUMP(APPLIC_TP_LOOP_START_%d);
        APPLIC_TP_LOOP_END_%d:
        DROP(R11);

        MOV(FP,R15);
        POP(R11);
        POP(R12);
        POP(R13);
        POP(R14);
        POP(R15);
        JUMPA (INDD(R0,2));
        // applicTP no. %d end here
        '''%(len(self.param),lnum,lnum,lnum,lnum,lnum)
        return res



class AsStringVisitor():
    def visitDef(self):
        return '(Define '+ str(self.var) +' '+ str(self.body)+')'
    def visitVar(self):
        return str(self.Var)
    def visitVarFree(self):
        return str(self.Var)
    def visitVarParam(self):
        return str(self.Var)
    def visitVarBound(self):
        return str(self.Var)
    def visitConst(self):
        if isinstance(self.con,sexprs.Symbol) or isinstance(self.con,sexprs.Nil) or  isinstance(self.con,sexprs.Pair) or isinstance (self.con,sexprs.Vector):
            return "'"+str(self.con)
        return str(self.con)
    def visitIfThenElse(self):
        res= '(If '+str(self.Condition)+ ' ' +str(self.Then)
        if isinstance(self.Else,Constant) and isinstance(self.Else.con,sexprs.Void):
            return res + ')'
        return res + ' ' + str(self.Else) + ')'
    def visitLambdaSimple(self):
        return '(Lambda ' +'('+ printArray(self.param)+ ') '+ str(self.body) + ')'
    def visitLambdaOpt(self):
        return '(Lambda ' +'('+ printArray(self.param)+' . '+str(self.opt)+') ' + str(self.body) + ')'
    def visitLambdaVar(self):
        res=str(self.param)
        if isinstance(self.param,Constant)and isinstance (self.param.con,sexprs.Nil):
            res="()"
        return '(Lambda '+res +' '+ str(self.body)+ ')'
    def visitOr(self):
        return '(Or '+ printArray(self.param) +')'
    def visitApplic(self):
        res= "("+str(self.applic)
        if len(self.param)!=0:
            res=res+" "
        res=res+printArray(self.param)+")"
        return res
    def visitApplicTP(self):
        res= "("+str(self.applic)
        if len(self.param)!=0:
            res=res+" "
        res=res+printArray(self.param)+")"
        return res

class Constant(AbstractSchemeExpr):
    def __init__(self,con):
        self.con=con
        self.ref=0

    def accept(self, v):
        return v.visitConst(self)

class Variable(AbstractSchemeExpr):
    def __init__(self,Var):
        self.Var=Var

    def accept(self, v):
        return v.visitVar(self)

    def isequal (self,other):
        if isinstance(other,Variable):
            if self.Var.string == other.Var.string:
                return True
        return False

class VarFree(Variable):
    def __init__(self,var):
        super().__init__(var.Var)

    def accept(self, v):
        return v.visitVarFree(self)

class VarParam(Variable):
    def __init__(self,var,pMinor):
        super().__init__(var.Var)
        self.minor=pMinor

    def accept(self, v):
        return v.visitVarParam(self)

class VarBound(Variable):
    def __init__(self,var,bMajor,bMinor):
        super().__init__(var.Var)
        self.major=bMajor
        self.minor=bMinor

    def accept(self, v):
        return v.visitVarBound(self)

class IfThenElse(AbstractSchemeExpr):
    def __init__(self,s_exp):
        if isinstance(s_exp,sexprs.Pair):
            self.Condition=AbstractSchemeExpr.parse_after_reader(s_exp.first)
            s_exp=s_exp.second
            if isinstance(s_exp,sexprs.Pair):
                self.Then=AbstractSchemeExpr.parse_after_reader(s_exp.first)
                s_exp=s_exp=s_exp.second
                if isinstance(s_exp,sexprs.Pair):
                    self.Else=AbstractSchemeExpr.parse_after_reader(s_exp.first)
                else:
                    self.Else=Constant(sexprs.Void())

    def accept(self, v):
        return v.visitIfThenElse(self)

class AbstractLambda(AbstractSchemeExpr):
    def __init__(self):
        self.env_size=0

class LambdaSimple(AbstractLambda):
    def __init__(self,s_exp):
        super().__init__()
        self.param=[]
        paramlist=s_exp.first
        while isinstance(paramlist,sexprs.Pair):
            self.param.append(AbstractSchemeExpr.parse_after_reader(paramlist.first))
            paramlist=paramlist.second
        if isinstance(s_exp.second,sexprs.Pair):
            self.body=AbstractSchemeExpr.parse_after_reader(s_exp.second.first)
        else:
            self.body=AbstractSchemeExpr.parse_after_reader(s_exp.second)
    def accept(self, v):
        return v.visitLambdaSimple(self)

class LambdaOpt(AbstractLambda):
    def __init__(self,s_exp):
        super().__init__()
        self.param=[]
        paramlist=s_exp.first
        while isinstance (paramlist,sexprs.Pair):
            self.param.append(AbstractSchemeExpr.parse_after_reader(paramlist.first))
            paramlist=paramlist.second
        self.opt=AbstractSchemeExpr.parse_after_reader(paramlist)
        if isinstance(s_exp.second,sexprs.Pair):
            self.body=AbstractSchemeExpr.parse_after_reader(s_exp.second.first)
        else:
            self.body=AbstractSchemeExpr.parse_after_reader(s_exp.second)

    def accept(self, v):
        return v.visitLambdaOpt(self)

class LambdaVar(AbstractLambda):
    def __init__(self,s_exp):
        super().__init__()
        self.param=AbstractSchemeExpr.parse_after_reader(s_exp.first)
        if isinstance(s_exp.second,sexprs.Pair):
            self.body=AbstractSchemeExpr.parse_after_reader(s_exp.second.first)
        else:
            self.body=AbstractSchemeExpr.parse_after_reader(s_exp.second)

    def accept(self, v):
        return v.visitLambdaVar(self)

class Applic(AbstractSchemeExpr):
    def __init__(self,s_exp):
        if isinstance(s_exp,sexprs.AbstractSexpr):
            self.applic=AbstractSchemeExpr.parse_after_reader(s_exp.first)
            self.param=[]
            s_exp=s_exp.second
            while isinstance(s_exp,sexprs.Pair):
                self.param.append(AbstractSchemeExpr.parse_after_reader(s_exp.first))
                s_exp=s_exp.second
            if not isinstance(s_exp, sexprs.Nil):
                self.param.append(AbstractSchemeExpr.parse_after_reader(s_exp))
        else:
            self.applic=s_exp.applic
            self.param=s_exp.param

    def accept(self, v):
        return v.visitApplic(self)

class ApplicTP(Applic):
    def __init__(self,s_exp):
        super().__init__(s_exp)

    def accept(self, v):
        return v.visitApplicTP(self)


class Or(AbstractSchemeExpr):
    def __init__(self,s_exp):
        self.param=[]
        while isinstance(s_exp,sexprs.Pair):
            self.param.append(AbstractSchemeExpr.parse_after_reader(s_exp.first))
            s_exp=s_exp.second
        if not isinstance(s_exp, sexprs.Nil):
            self.param.append(AbstractSchemeExpr.parse_after_reader(s_exp))

    def accept(self, v):
        return v.visitOr(self)

class Def(AbstractSchemeExpr):
    def __init__(self,s_exp):
        if isinstance(s_exp,sexprs.Pair):
            if isinstance(s_exp.first,sexprs.Pair):
                self.var=AbstractSchemeExpr.parse_after_reader(s_exp.first.first)
                rest=sexprs.Pair(s_exp.first.second,s_exp.second)
                rest=sexprs.Pair(sexprs.Symbol('LAMBDA'),rest)
                self.body=AbstractSchemeExpr.parse_after_reader(rest)
            else:
                self.var=AbstractSchemeExpr.parse_after_reader(s_exp.first)
                self.body=AbstractSchemeExpr.parse_after_reader(s_exp.second.first)

    def accept(self, v):
        return v.visitDef(self)

def Quote(s_exp):
    return Constant(s_exp.first)

def vectorToList(s_exp):
    elem=s_exp.elements
    if len(elem)==0:
        return sexprs.Nil()
    return sexprs.Pair(elem[0],vectorToList(elem[1:]))
def QQ_expend_first_only (s_exp):
    #return AbstractSchemeExpr.parse_after_reader(QQ_expend(s_exp.first))
    return QQ_expend(s_exp.first)

def listToVector(s_exp):
    res=[]
    while not isinstance(s_exp, sexprs.Nil):
        res.append(s_exp.first)
    return sexprs.Vector(res)

def QQ_expend(s_exp):
    if isinstance(s_exp,sexprs.Pair):
        if isinstance(s_exp.first,sexprs.Symbol) and  isinstance(s_exp.second,sexprs.Pair):
            if s_exp.first.string=="unquote":
                return s_exp.second.first
            elif s_exp.first.string=="unquote-splicing":
                raise (Exception("unquote-splicing here makes no sense!"))
        a=s_exp.first
        b=s_exp.second
        if isinstance(a,sexprs.Pair) and isinstance(a.first,sexprs.Symbol) and a.first.string=="unquote-splicing":
            if isinstance(b, sexprs.Nil):
                return a.second.first
            return sexprs.Pair(sexprs.Symbol('APPEND'), sexprs.Pair(a.second.first
                    , sexprs.Pair(QQ_expend(b), sexprs.Nil())))
        elif isinstance(b,sexprs.Pair) and isinstance(b.first,sexprs.Symbol) and b.first.string=="unquote-splicing":
            return sexprs.Pair(sexprs.Symbol('CONS'), sexprs.Pair(QQ_expend(a)
                    , sexprs.Pair(b.second.first, sexprs.Nil())))
        return sexprs.Pair(sexprs.Symbol('CONS'), sexprs.Pair(QQ_expend(a)
                    , sexprs.Pair(QQ_expend(b), sexprs.Nil())))
    elif isinstance(s_exp,sexprs.Vector):
        return sexprs.Pair(sexprs.Symbol("LIST->VECTOR") , sexprs.Pair(QQ_expend(vectorToList(s_exp)),sexprs.Nil()))
    elif isinstance(s_exp,sexprs.Nil) or isinstance(s_exp,sexprs.Symbol):
        return sexprs.Pair(sexprs.Symbol("quote"), sexprs.Pair(s_exp,sexprs.Nil()))
    return s_exp

schemeWords = {
    'DEFINE' : Def,
    'LAMBDA' : AbstractSchemeExpr.Lambdacheck,
    'IF' : IfThenElse,
    'OR' : checkOr,
    'quote':Quote,


}

syntaticWords={
    'COND': condToIf,
    'AND': andToIf,
    'LET': letToApplic,
    'LET*': letStarToApplic,
    'LETREC' : letToYagApplic,
    'quasiquote':QQ_expend_first_only,
}

class Const_table:
    const_table=[]
    @staticmethod
    def const_init():
        Const_table.const_table=[]
        Const_table.const_table.append(7)
        Const_table.const_table.append('T_VOID')
        Const_table.const_table.append('T_NIL')
        #True at 3
        Const_table.const_table.append('T_BOOL')
        Const_table.const_table.append('1')
        #false at 5
        Const_table.const_table.append('T_BOOL')
        Const_table.const_table.append('0')

    @staticmethod
    def create_const_table(s_exp):
        exist=False
        notExist=True
        if isinstance(s_exp,AbstractLambda):
            s_exp.body = Const_table.create_const_table(s_exp.body)

        elif isinstance(s_exp,Def):
            s_exp.var = Const_table.create_const_table(sexprs.Symbol(s_exp.var.Var.string.upper()))
            s_exp.body = Const_table.create_const_table(s_exp.body)

        elif isinstance(s_exp,Or):
            for x in s_exp.param:
                x = Const_table.create_const_table(x)

        elif isinstance(s_exp,Constant):
            s_exp.con = Const_table.create_const_table(s_exp.con)
            s_exp.ref=s_exp.con.ref
        if isinstance(s_exp,sexprs.Void):
            s_exp.ref=1
        elif isinstance(s_exp,sexprs.Nil):
            s_exp.ref=2
        elif isinstance(s_exp,sexprs.true):
            s_exp.ref=3
        elif isinstance(s_exp,sexprs.false):
            s_exp.ref=5
        elif isinstance(s_exp,IfThenElse):
            Const_table.create_const_table(s_exp.Condition)
            Const_table.create_const_table(s_exp.Then)
            Const_table.create_const_table(s_exp.Else)

        elif isinstance(s_exp,Applic):
            Const_table.create_const_table(s_exp.applic)
            for x in s_exp.param:
                Const_table.create_const_table(x)
        elif isinstance(s_exp,VarFree):
            s_exp.Var=Const_table.create_const_table(s_exp.Var)
        elif isinstance (s_exp,sexprs.Char):
            for x in range(1,len(Const_table.const_table)):
                if Const_table.const_table[x] == 'T_CHAR':
                    if Const_table.const_table[x+1] == s_exp.char:
                        notExist=False
                        s_exp.ref=x
            if notExist:
                s_exp.ref=Const_table.const_table[0]
                Const_table.const_table.append('T_CHAR')
                if s_exp.char == 'newline':
                    Const_table.const_table.append(10)
                elif s_exp.char == 'page':
                    Const_table.const_table.append(12)
                elif s_exp.char == 'return':
                    Const_table.const_table.append(13)
                elif s_exp.char == 'tab':
                    Const_table.const_table.append(9)
                elif s_exp.char == 'lambda':
                    Const_table.const_table.append(0x03bb)
                else:
                    Const_table.const_table.append(ord(s_exp.char))
                Const_table.const_table[0]+=2

        elif isinstance (s_exp,sexprs.Symbol):
            temp = sexprs.String(s_exp.string);
            temp= Const_table.create_const_table(temp);
            for x in range(1,len(Const_table.const_table)):
                if Const_table.const_table[x] == 'T_SYMBOL':
                    if Const_table.const_table[x+1] == temp.ref:
                        notExist=False
                        s_exp.ref=x
            if notExist:
                s_exp.ref=Const_table.const_table[0]
                Const_table.const_table.append('T_SYMBOL')
                Const_table.const_table.append(temp.ref)
                Const_table.const_table[0]+=2

        elif isinstance (s_exp,sexprs.String):
            for x in range(1,len(Const_table.const_table)):
                if Const_table.const_table[x] == 'T_STRING':
                    temp_symbol=""
                    for i in range(1,int(Const_table.const_table[x+1]+1)):
                        temp_symbol+=chr(Const_table.const_table[x+1+i])
                    if temp_symbol == s_exp.string:
                        notExist=False
                        s_exp.ref=x
            if notExist:
                s_exp.ref=Const_table.const_table[0]
                Const_table.const_table.append('T_STRING')
                Const_table.const_table.append(s_exp.length)
                Const_table.const_table[0]+=2+s_exp.length
                for x in range (0,s_exp.length):
                    Const_table.const_table.append(ord(s_exp.string[x]))


        elif isinstance(s_exp,sexprs.Integer):
            for x in range(1,len(Const_table.const_table)):
                if Const_table.const_table[x] == 'T_INTEGER':
                    if Const_table.const_table[x+1] == s_exp.number:
                        exist = True
                        s_exp.ref=x
            if not exist:
                s_exp.ref=Const_table.const_table[0]
                Const_table.const_table.append('T_INTEGER')
                Const_table.const_table.append(s_exp.number)
                Const_table.const_table[0]+=2

        elif isinstance (s_exp,sexprs.Fraction):
            for x in range(1,len(Const_table.const_table)):
                if Const_table.const_table[x] == 'T_FRACTION':
                    if Const_table.const_table[x+1] == s_exp.nume:
                        if Const_table.const_table[x+2] == s_exp.deno:
                            exist = True
                            s_exp.ref=x
            if not exist:
                s_exp.ref=Const_table.const_table[0]
                Const_table.const_table.append('T_FRACTION')
                Const_table.const_table.append(s_exp.nume)
                Const_table.const_table.append(s_exp.deno)
                Const_table.const_table[0]+=3

        elif isinstance(s_exp,sexprs.Pair):
                s_exp.second = Const_table.create_const_table(s_exp.second)
                s_exp.first = Const_table.create_const_table(s_exp.first)

                for x in range(1,len(Const_table.const_table)):
                    if Const_table.const_table[x] == 'T_PAIR':
                        if Const_table.const_table[x+1] == s_exp.first.ref:
                            if Const_table.const_table[x+2] == s_exp.second.ref:
                                exist = True
                                s_exp.ref=x
                if not exist:
                    s_exp.ref=Const_table.const_table[0]
                    Const_table.const_table.append('T_PAIR')
                    Const_table.const_table.append(s_exp.first.ref)
                    Const_table.const_table.append(s_exp.second.ref)
                    Const_table.const_table[0] += 3

        elif isinstance(s_exp,sexprs.Vector):
            for x in range (0,len(s_exp.elements)):
                s_exp.elements[x]=Const_table.create_const_table(s_exp.elements[x])
            for x in range(1,len(Const_table.const_table)):
                    if Const_table.const_table[x] == 'T_VECTOR':
                        if Const_table.const_table[x+1] == s_exp.length:
                            all=True
                            for y in range (0,len(s_exp.elements)):
                                if Const_table.const_table[x+y+2] != s_exp.elements[y].ref:
                                    all=False
                            if all:
                                exist = True
                                s_exp.ref=x
            if not exist:
                Const_table.const_table.append('T_VECTOR')
                Const_table.const_table.append(s_exp.length)
                s_exp.ref=Const_table.const_table[0]
                start_pos=Const_table.const_table[0]+2
                Const_table.const_table[0] += 2 + s_exp.length
                for i in range (0,s_exp.length):
                    Const_table.const_table.append(0)
                i=0;
                for x in s_exp.elements:
                    temp= Const_table.create_const_table(x)
                    Const_table.const_table[start_pos+i]=(temp.ref)
                    i=i+1


        return s_exp
