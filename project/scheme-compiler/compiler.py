# coding=utf8   
import tag_parser


def print_begin():
    return '''
#include <stdio.h>
#include <stdlib.h>
#define DO_SHOW 1
#include "arch/cisc.h"

#define FALSE_CONSTANT 5
#define TRUE_CONSTANT 3
#define NIL_CONSTANT 2

//LOCAL (0) IS RESERVED FOR THE BUCKET LIST POINTER
int main()
{
START_MACHINE;
//CALL (INITIAL_START);
JUMP(CONTINUE);

#include "arch/char.lib"
#include "arch/io.lib"
#include "arch/math.lib"
#include "arch/string.lib"
#include "arch/system.lib"
#include "arch/scheme.lib"

    //find or create bucket:
    //FPARG(0) = T_STRING ref
    find_or_create_bucket:
    BEGIN_LOCAL_LABELS bucket_search_loop ,create_new_bucket, bucket_end;
    PUSH (FP);
    MOV (FP,SP);
    PUSH(R4);
    //search for bucket
    MOV (R4,IND('''+str(tag_parser.Const_table.const_table[0])+'''));
    bucket_search_loop:
    CMP(R4,0);
    MOV(R0,R4);
    JUMP_EQ(create_new_bucket);
    CMP(IND(R4),FPARG(0));
    JUMP_EQ (bucket_end);
    MOV(R4,INDD(R4,2));
    JUMP (bucket_search_loop);

    //a bucket was not found so create new one
    create_new_bucket:
    PUSH (3);
    CALL (MALLOC);
    DROP(1);
    MOV(INDD(R0,2),IND('''+str(tag_parser.Const_table.const_table[0])+'''));
    MOV(IND('''+str(tag_parser.Const_table.const_table[0])+'''),R0);

    bucket_end:
    POP(R4);
    POP(FP);
    RETURN;
    END_LOCAL_LABELS;

    FIND_BUCKET_WITH_SAME_NAME:
    BEGIN_LOCAL_LABELS FIND_BUCKET_LOOP , FIND_BUCKET_END;
    PUSH (FP);
    MOV (FP,SP);
    //search for bucket
    MOV (R0,IND('''+str(tag_parser.Const_table.const_table[0])+'''));
    FIND_BUCKET_LOOP:

    CMP(IND(R0),FPARG(0));
    JUMP_EQ(FIND_BUCKET_END);
    MOV(R0,INDD(R0,2));
    JUMP (FIND_BUCKET_LOOP);
    FIND_BUCKET_END:
    POP(FP);
    RETURN;
    END_LOCAL_LABELS;



   //COPY ENV FUNCTION - FP(0) = NEW ADDRESS , FP(1) = OLD ENV , FP(2) = OLD ENV SIZE

   BEGIN_LOCAL_LABELS COPY_ENV_START, COPY_ENV_END, COPY_ENV_LOOP;
   COPY_ENV:
   PUSH (FP);
   MOV (FP,SP);
   COPY_ENV_START:
   PUSH(R1);
   PUSH(R2);
   PUSH(R3);
   MOV (R0, FPARG(0));
   MOV (R1, FPARG(1));
   MOV (R2, FPARG(2));
   MOV (R3,0);
   MOV (R4,1);
   COPY_ENV_LOOP:
   CMP(R2,0);
   JUMP_EQ(COPY_ENV_END);

   MOV (INDD (R0 , R4 ) , INDD(R1,R3));
   ADD (R3,IMM(1));
   ADD (R4,IMM(1));
   SUB (R2,IMM(1));
   JUMP (COPY_ENV_LOOP);
   COPY_ENV_END:
   POP(R3);
   POP(R2);
   POP(R1);
   POP(FP);
   RETURN;
   END_LOCAL_LABELS;

CONTINUE:
'''


def make_bucket_to_all_symbols():
    res=""
    for x in range(1,len(tag_parser.Const_table.const_table)):
        if tag_parser.Const_table.const_table[x] == 'T_SYMBOL':
            lnum= tag_parser.lableCount.newLableNumber()
            res+='''
            MOV(R0,%d); // puts in r0 a pointer to T_symbol successor
            CMP (IND(R0),T_STRING);
            JUMP_NE(SYMBOL_CHECK_BUCKET_END_%d);
            PUSH (%d); //push the represnted string.
            CALL (find_or_create_bucket);
            DROP(1);
            //now we have a bucket we put the string and the data inside.
            MOV (IND(R0),%d); // put string in place
            //make the symbol in the const table to point the bucket:
            MOV (IND(%d),R0);
            SYMBOL_CHECK_BUCKET_END_%d:
            NOP;
            '''%(tag_parser.Const_table.const_table[x+1],lnum,tag_parser.Const_table.const_table[x+1],tag_parser.Const_table.const_table[x+1],x+1,lnum)
    return res



def const_python_to_asm():
  res=""
  for i in range(0,len(tag_parser.Const_table.const_table)):
    res += "MOV(IND(%d) , %s);\n"%(i,tag_parser.Const_table.const_table[i])
  return res

def printMem(a=0,b=0):
  res=""
  for i in range (a,b):
    res+='SHOW ("mem[%d]",IND(%d));\n'%(i,i)
  return res

def create_specific_basic_func(str1,char1,leng):
    res='''
    PUSH(R1);
    PUSH (LABEL(%s));
    PUSH (0);
    CALL (MAKE_SOB_CLOSURE);
    DROP(2);
    MOV(R1,R0); //r1 points to the T_closure
    '''%(str1)
    temp_ref=0;
    found=False;
    for x in range(1,len(tag_parser.Const_table.const_table)):
            if tag_parser.Const_table.const_table[x] == 'T_STRING':
                if tag_parser.Const_table.const_table[x+1]==leng:
                    match=True
                    for y in range(0,leng):
                        if match:
                            if tag_parser.Const_table.const_table[x+2+y] != ord(char1[y]):
                                match=False
                    if match:
                        temp_ref=x;
    res+='''
    PUSH (%d);
    CALL (FIND_BUCKET_WITH_SAME_NAME);
    DROP(1);
    //now r0 points to bucket;
    MOV(INDD(R0,1),R1);
    POP(R1);
    '''%(temp_ref)
    return res

def create_all_basic_func():
    res= create_specific_basic_func("PLUS","+",1)
    res+= create_specific_basic_func("MULTIPLICITY","*",1)
    res+= create_specific_basic_func("MINUS","-",1)
    res+= create_specific_basic_func("DIVIDE","/",1)
    res+= create_specific_basic_func("LESS_THEN","<",1)
    res+= create_specific_basic_func("GREATER_THEN",">",1)
    res+= create_specific_basic_func("CAR","CAR",3)
    res+= create_specific_basic_func("CDR","CDR",3)
    res+= create_specific_basic_func("CONS","CONS",4)
    res+= create_specific_basic_func("EQUAL","=",1)
    res+= create_specific_basic_func("ZERO","ZERO?",5)
    res+= create_specific_basic_func("BOOLEAN","BOOLEAN?",8)
    res+= create_specific_basic_func("INTEGER","INTEGER?",8)
    res+= create_specific_basic_func("NUMBER","NUMBER?",7)
    res+= create_specific_basic_func("CHAR","CHAR?",5)
    res+= create_specific_basic_func("VECTOR","VECTOR?",7)
    res+= create_specific_basic_func("IS_NULL","NULL?",5)
    res+= create_specific_basic_func("PAIR","PAIR?",5)
    res+= create_specific_basic_func("PROCEDURE","PROCEDURE?",10)
    res+= create_specific_basic_func("STRING","STRING?",7)
    res+= create_specific_basic_func("SYMBOL","SYMBOL?",7)
    res+= create_specific_basic_func("EQ","EQ?",3)
    res+= create_specific_basic_func("LIST","LIST",4)
    res+= create_specific_basic_func("REMAINDER","REMAINDER",9)
    res+= create_specific_basic_func("APPEND","APPEND",6)
    res+= create_specific_basic_func("STRING_REF","STRING-REF",10)
    res+= create_specific_basic_func("VECTOR_REF","VECTOR-REF",10)
    res+= create_specific_basic_func("STRING_LENGTH","STRING-LENGTH",13)
    res+= create_specific_basic_func("VECTOR_LENGTH","VECTOR-LENGTH",13)
    res+= create_specific_basic_func("CHAR_TO_INT","CHAR->INTEGER",13)
    res+= create_specific_basic_func("INT_TO_CHAR","INTEGER->CHAR",13)
    res+= create_specific_basic_func("MAKE_STRING","MAKE-STRING",11)
    res+= create_specific_basic_func("MAKE_VECTOR","MAKE-VECTOR",11)
    res+= create_specific_basic_func("CREATE_VECTOR","VECTOR",6)
    res+= create_specific_basic_func("LIST_TO_VECTOR","LIST->VECTOR",12)
    res+= create_specific_basic_func("SYMBOL_STRING","SYMBOL->STRING",14)
    res+= create_specific_basic_func("STRING_SYMBOL","STRING->SYMBOL",14)
    res+= create_specific_basic_func("MAP","MAP",3)
    res+= create_specific_basic_func("APPLY","APPLY",5)
    return res








def compile_scheme_file (source , target):
    tag_parser.Const_table.const_init()

    b1="(define + \'())"
    b2="(define * \'())"
    b3="(define - \'())"
    b4="(define / \'())"
    b5="(define < \'())"
    b6="(define > \'())"
    b7="(define CAR \'())"
    b8="(define CDR \'())"
    b9="(define CONS \'())"
    b10="(define = \'())"
    b11="(define ZERO? \'())"
    b12="(define BOOLEAN? \'())"
    b13="(define INTEGER? \'())"
    b14="(define NUMBER? \'())"
    b15="(define CHAR? \'())"
    b16="(define VECTOR? \'())"
    b17="(define NULL? \'())"
    b18="(define PAIR? \'())"
    b19="(define PROCEDURE? \'())"
    b20="(define STRING? \'())"
    b21="(define SYMBOL? \'())"
    b22="(define EQ? \'())"
    b23="(define LIST \'())"
    b24="(define REMAINDER \'())"
    b25="(define APPEND \'())"
    b26="(define STRING-LENGTH \'())"
    b27="(define VECTOR-LENGTH \'())"
    b28="(define STRING-REF \'())"
    b29="(define VECTOR-REF \'())"
    b30="(define CHAR->INTEGER \'())"
    b31="(define INTEGER->CHAR \'())"
    b32="(define MAKE-STRING \'())"
    b33="(define MAKE-VECTOR \'())"
    b34="(define VECTOR \'())"
    b35="(define LIST->VECTOR \'())"
    b36="(define SYMBOL->STRING \'())"
    b37="(define STRING->SYMBOL \'())"
    b38="(define MAP \'())"
    b39="(define APPLY \'())"
    b40='''
    (define YAG
        (lambda fs
            (let ((ms (map
                (lambda (fi)
                  (lambda ms
                    (apply fi (map (lambda (mi)
                             (lambda args
                               (apply (apply mi ms) args))) ms))))
                fs)))
              (apply (car ms) ms))))
    '''

    b,aa=tag_parser.AbstractSchemeExpr.parse(b1)
    c,aa=tag_parser.AbstractSchemeExpr.parse(b2)
    d,aa=tag_parser.AbstractSchemeExpr.parse(b3)
    e,aa=tag_parser.AbstractSchemeExpr.parse(b4)
    f,aa=tag_parser.AbstractSchemeExpr.parse(b5)
    g,aa=tag_parser.AbstractSchemeExpr.parse(b6)
    h,aa=tag_parser.AbstractSchemeExpr.parse(b7)
    i,aa=tag_parser.AbstractSchemeExpr.parse(b8)
    j,aa=tag_parser.AbstractSchemeExpr.parse(b9)
    k,aa=tag_parser.AbstractSchemeExpr.parse(b10)
    l,aa=tag_parser.AbstractSchemeExpr.parse(b11)
    m,aa=tag_parser.AbstractSchemeExpr.parse(b12)
    n,aa=tag_parser.AbstractSchemeExpr.parse(b13)
    o,aa=tag_parser.AbstractSchemeExpr.parse(b14)
    p,aa=tag_parser.AbstractSchemeExpr.parse(b15)
    q,aa=tag_parser.AbstractSchemeExpr.parse(b16)
    r,aa=tag_parser.AbstractSchemeExpr.parse(b17)
    s,aa=tag_parser.AbstractSchemeExpr.parse(b18)
    t,aa=tag_parser.AbstractSchemeExpr.parse(b19)
    u,aa=tag_parser.AbstractSchemeExpr.parse(b20)
    v,aa=tag_parser.AbstractSchemeExpr.parse(b21)
    w,aa=tag_parser.AbstractSchemeExpr.parse(b22)
    x,aa=tag_parser.AbstractSchemeExpr.parse(b23)
    y,aa=tag_parser.AbstractSchemeExpr.parse(b24)
    z,aa=tag_parser.AbstractSchemeExpr.parse(b25)
    za,aa=tag_parser.AbstractSchemeExpr.parse(b26)
    zb,aa=tag_parser.AbstractSchemeExpr.parse(b27)
    zc,aa=tag_parser.AbstractSchemeExpr.parse(b28)
    zd,aa=tag_parser.AbstractSchemeExpr.parse(b29)
    ze,aa=tag_parser.AbstractSchemeExpr.parse(b30)
    zf,aa=tag_parser.AbstractSchemeExpr.parse(b31)
    zg,aa=tag_parser.AbstractSchemeExpr.parse(b32)
    zh,aa=tag_parser.AbstractSchemeExpr.parse(b33)
    zi,aa=tag_parser.AbstractSchemeExpr.parse(b34)
    zj,aa=tag_parser.AbstractSchemeExpr.parse(b35)
    zk,aa=tag_parser.AbstractSchemeExpr.parse(b36)
    zl,aa=tag_parser.AbstractSchemeExpr.parse(b37)
    zm,aa=tag_parser.AbstractSchemeExpr.parse(b38)
    zn,aa=tag_parser.AbstractSchemeExpr.parse(b39)
    zo,aa=tag_parser.AbstractSchemeExpr.parse(b40)

    b=b.semantic_analysis()
    b=tag_parser.Const_table.create_const_table(b)
    c=c.semantic_analysis()
    c=tag_parser.Const_table.create_const_table(c)
    d=d.semantic_analysis()
    d=tag_parser.Const_table.create_const_table(d)
    e=e.semantic_analysis()
    e=tag_parser.Const_table.create_const_table(e)
    f=f.semantic_analysis()
    f=tag_parser.Const_table.create_const_table(f)
    g=g.semantic_analysis()
    g=tag_parser.Const_table.create_const_table(g)
    h=h.semantic_analysis()
    h=tag_parser.Const_table.create_const_table(h)
    i=i.semantic_analysis()
    i=tag_parser.Const_table.create_const_table(i)
    j=j.semantic_analysis()
    j=tag_parser.Const_table.create_const_table(j)
    k=k.semantic_analysis()
    k=tag_parser.Const_table.create_const_table(k)
    l=l.semantic_analysis()
    l=tag_parser.Const_table.create_const_table(l)
    m=m.semantic_analysis()
    m=tag_parser.Const_table.create_const_table(m)
    n=n.semantic_analysis()
    n=tag_parser.Const_table.create_const_table(n)
    o=o.semantic_analysis()
    o=tag_parser.Const_table.create_const_table(o)
    p=p.semantic_analysis()
    p=tag_parser.Const_table.create_const_table(p)
    q=q.semantic_analysis()
    q=tag_parser.Const_table.create_const_table(q)
    r=r.semantic_analysis()
    r=tag_parser.Const_table.create_const_table(r)
    s=s.semantic_analysis()
    s=tag_parser.Const_table.create_const_table(s)
    t=t.semantic_analysis()
    t=tag_parser.Const_table.create_const_table(t)
    u=u.semantic_analysis()
    u=tag_parser.Const_table.create_const_table(u)
    v=v.semantic_analysis()
    v=tag_parser.Const_table.create_const_table(v)
    w=w.semantic_analysis()
    w=tag_parser.Const_table.create_const_table(w)
    x=x.semantic_analysis()
    x=tag_parser.Const_table.create_const_table(x)
    y=y.semantic_analysis()
    y=tag_parser.Const_table.create_const_table(y)
    z=z.semantic_analysis()
    z=tag_parser.Const_table.create_const_table(z)
    za=za.semantic_analysis()
    za=tag_parser.Const_table.create_const_table(za)
    zb=zb.semantic_analysis()
    zb=tag_parser.Const_table.create_const_table(zb)
    zc=zc.semantic_analysis()
    zc=tag_parser.Const_table.create_const_table(zc)
    zd=zd.semantic_analysis()
    zd=tag_parser.Const_table.create_const_table(zd)
    ze=ze.semantic_analysis()
    ze=tag_parser.Const_table.create_const_table(ze)
    zf=zf.semantic_analysis()
    zf=tag_parser.Const_table.create_const_table(zf)
    zg=zg.semantic_analysis()
    zg=tag_parser.Const_table.create_const_table(zg)
    zh=zh.semantic_analysis()
    zh=tag_parser.Const_table.create_const_table(zh)
    zi=zi.semantic_analysis()
    zi=tag_parser.Const_table.create_const_table(zi)
    zj=zj.semantic_analysis()
    zj=tag_parser.Const_table.create_const_table(zj)
    zk=zk.semantic_analysis()
    zk=tag_parser.Const_table.create_const_table(zk)
    zl=zl.semantic_analysis()
    zl=tag_parser.Const_table.create_const_table(zl)
    zm=zm.semantic_analysis()
    zm=tag_parser.Const_table.create_const_table(zm)
    zn=zn.semantic_analysis()
    zn=tag_parser.Const_table.create_const_table(zn)
    zo=zo.semantic_analysis()
    zo=tag_parser.Const_table.create_const_table(zo)
    array=[]
    finput = open (source,'r')
    inputString=finput.read()
    while inputString != "":
        a,inputString=tag_parser.AbstractSchemeExpr.parse(inputString)
        if a != None:
            a=a.semantic_analysis()
            a=tag_parser.Const_table.create_const_table(a)
            array.append(a)
    res=print_begin()
    temp=const_python_to_asm()+'''

    PUSH(1);
    CALL (MALLOC);
    DROP(1);
    MOV(IND(R0),0);
    MOV(SP,20);
    MOV(FP,20);
    //  now r0 hold the start of the bucket list
    //  its a place holder for the beginnning of the bucket list
    // now i push zeros in order to make lambda env work correctly.
    PUSH(IMM(0));
    PUSH(IMM(0));
    PUSH(IMM(0));
    PUSH(IMM(0));
    '''
    code=temp+\
    b.code_gen()+\
    c.code_gen()+\
    d.code_gen()+\
    e.code_gen()+\
    f.code_gen()+\
    g.code_gen()+\
    h.code_gen()+\
    i.code_gen()+\
    j.code_gen()+\
    k.code_gen()+\
    l.code_gen()+\
    m.code_gen()+\
    n.code_gen()+\
    o.code_gen()+\
    p.code_gen()+\
    q.code_gen()+\
    r.code_gen()+\
    s.code_gen()+\
    t.code_gen()+\
    u.code_gen()+\
    v.code_gen()+\
    w.code_gen()+\
    x.code_gen()+\
    y.code_gen()+\
    z.code_gen()+\
    za.code_gen()+\
    zb.code_gen()+\
    zc.code_gen()+\
    zd.code_gen()+\
    ze.code_gen()+\
    zf.code_gen()+\
    zg.code_gen()+\
    zh.code_gen()+\
    zi.code_gen()+\
    zj.code_gen()+\
    zk.code_gen()+\
    zl.code_gen()+\
    zm.code_gen()+\
    zn.code_gen()+\
    zo.code_gen()+\
    create_all_basic_func()+\
    make_bucket_to_all_symbols()+'\n'+\
        '''
    '''

    for x in range (0, len(array)):
        lnum= tag_parser.lableCount.newLableNumber()
        code+=array[x].code_gen()
        code+='''
        CMP (R0,IMM(1));
        JUMP_EQ(DONT_PRINT_RES_%d);
        PUSH (R0);
        CALL (WRITE_SOB);
        CALL (NEWLINE);
        DROP(1);
        DONT_PRINT_RES_%d:
        NOP;
        '''%(lnum,lnum)

    res+= code
    #res+=printMem(0,700)
    res+='''
    STOP_MACHINE;
    return 0;
    }
    '''
    fout = open(target , 'w')
    fout.write(res)
    finput.close()
    fout.close()